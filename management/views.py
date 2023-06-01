import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import BooleanField
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

from structures.models import DataStructure
from .forms import ManagementForm
from .models import Contract, Management
from .utils import convert_string_int_to_bool, convert_string, query_items, \
    check_required_field_to_management, convert_file_to_dictionary, convert_date_format, check_validation_on_management, \
    convert_string_to_int, check_header_in_structure

FormSet = formset_factory(ManagementForm, extra=0)


def custom_logout(request):
    logout(request)
    return redirect('upload_data')  # Redirect to the desired URL after logout


class ContractDeleteView(View):
    """
    this is used to delete a Contract
    """

    def post(self, request):
        #  this  deletes a redirect back to the page
        item_id = request.POST.get("contract_id")
        if item_id:
            history = Contract.objects.filter(id=item_id, user=self.request.user).first()
            if history:
                history.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ContractDetailView(LoginRequiredMixin, ListView):
    """
    this is the detail page of the contract
    """
    queryset = Management.objects.all()
    template_name = "management.html"
    paginate_by = 1000

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        id = self.kwargs['id']
        query = self.request.GET.get('search')

        contract = get_object_or_404(Contract, id=id)
        queryset = contract.management_set.all()
        ordering = self.get_ordering()
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Overiding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        context["contract_id"] = self.kwargs['id']
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        return context


class ContractUpdateView(LoginRequiredMixin, ListView):
    """
    This is used to view the excel page to update the document
    """
    queryset = Management.objects.all()
    template_name = "management_edit.html"
    paginate_by = 1000

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        id = self.kwargs['id']
        query = self.request.GET.get('search')

        contract = get_object_or_404(Contract, id=id)
        queryset = contract.management_set.all()
        ordering = self.get_ordering()
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Overiding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        # context['item_form'] = ManagementUpdate()
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        context["contract_id"] = self.kwargs['id']
        contract = Contract.objects.filter(id=self.kwargs['id']).first()

        #  new
        context["formset"] = [ManagementForm(instance=instance) for instance in contract.management_set.all()]
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        return context


class UpdateAllContractAPIView(View):
    """
    This view is used to update all fields from javasript post request using xml for the excel page
    """

    def post(self, request, id):
        contract_id = id
        # Check if the contract exists
        contract = Contract.objects.filter(id=contract_id).first()
        if not contract:
            return redirect("list_contract_management")

        # Retrieve the form data from the request body
        form_data = json.loads(request.body)

        # Perform the update operation for each form
        for form in form_data['forms']:
            form_id = form['id']
            form_fields = form['fields']

            # Retrieve the management instance based on the form ID
            management_instance = Management.objects.filter(id=form_id).first()
            if not management_instance:
                continue

            # Update the fields of the management instance
            for field_name, field_value in form_fields.items():
                #  if the  is among this just skip
                if field_name == "id" or field_name == "timestamp" or field_name == "user" or field_name == "contract":
                    continue
                #  if not value just skip
                if not field_value:
                    continue

                # Check if the field is a Boolean field
                field = Management._meta.get_field(field_name)
                if isinstance(field, BooleanField):
                    # Convert the field value to a Boolean
                    field_value = field_value.lower() == "true"

                if getattr(management_instance, field_name, field_value) != field_value:
                    # this set the attribute only if the value is not same with the old one and also saves it
                    setattr(management_instance, field_name, field_value)
            # Save the updated management instance for any update
            management_instance.save()

        return JsonResponse({'message': 'Update successful'})


class UploadContractView(LoginRequiredMixin, View):
    """
    this is used to upload excel spreadsheet which is then read and can be used to create tables

    """

    def get(self, request):
        # redirect the user to admin dashboard
        if request.user.is_staff or request.user.is_superuser:
            return redirect("admin_dashboard")
        # create the structure for the user if not exists
        if not DataStructure.objects.filter(user=self.request.user).first():
            DataStructure.objects.create(user=self.request.user)
        # get the contract
        contracts = Contract.objects.filter(user=self.request.user)
        context = {
            "contracts": contracts,
        }
        return render(request, "index.html", context)

    def post(self, request):
        global contract
        if request.method == 'POST' and request.FILES['property_file']:
            property_file = request.FILES['property_file']
            contract_name = request.POST.get("name")
            data_structure_id = DataStructure.objects.filter(user=self.request.user).first().id

            if not contract_name or not property_file or not data_structure_id:
                messages.warning(request, "Contract name or Excel File is required")
                return redirect("upload_data")

            try:
                contract = Contract.objects.create(name=contract_name, user=self.request.user)
                structure = DataStructure.objects.filter(id=data_structure_id, user=self.request.user).first()

                property_datas = convert_file_to_dictionary(property_file)
                #  validate the headers
                headers = property_datas[0].keys()
                error_list = check_header_in_structure(headers=headers, structure=structure)
                # loop through the property data
                for data in property_datas:
                    management = Management()

                    for field in structure._meta.get_fields():
                        if field.name == "id" or field.name == "timestamp" or field.name == "user" or field.name == "contract":
                            continue

                        field_name = field.name
                        user_field_name = getattr(structure, field_name)
                        converted_field_name = convert_string(user_field_name)
                        management_value = data.get(converted_field_name)

                        #  we get attribute to be able to set the right value
                        if isinstance(management._meta.get_field(field_name), models.BooleanField):
                            setattr(management, field_name, convert_string_int_to_bool(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.DateField):
                            setattr(management, field_name, convert_date_format(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.DecimalField):

                            setattr(management, field_name, convert_string_to_int(management_value))
                        else:
                            setattr(management, field_name, management_value)

                    management.contract = contract
                    management.user = self.request.user
                    management.save()

                # loop through the error for header check
                for item in error_list:
                    messages.error(request, item)
                    # if the error is too much redirect back to home page to upload again
                    if len(error_list) > 15:
                        contract.delete()
                        return redirect("upload_data")
                return redirect("validate_contract", contract.id)
            except Exception as e:
                contract.delete()
                messages.error(request, f'Error uploading file: {e}')
                return redirect("upload_data")
        return redirect("upload_data")


class ValidateContractView(LoginRequiredMixin, View):
    """
    this view is handling the validation of a contract, and it redirects the user to either the detail page or the
    update page base on the status of the contract
    """

    def get(self, request, id):
        contract = Contract.objects.filter(id=id).first()
        if not id:
            # redirect back to the page which  it comes from
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        errors = []
        # First we check for required fields
        check_errors = check_required_field_to_management(contract)
        # user custom validation
        validate_errors = check_validation_on_management(contract)
        #  check if the length of the error is greater than zero if it is then
        #  we need to direct the user to the update page
        errors += check_errors
        errors += validate_errors
        if len(errors) > 0:
            contract.status = "PENDING"
            contract.save()
            for error in errors:
                messages.error(request, error)
            return redirect("contract_update", contract.id)
        contract.status = "SUCCESS"
        contract.save()
        messages.info(request, "The contract has been validated and is error-free.")
        return redirect("contract_detail", contract.id)
