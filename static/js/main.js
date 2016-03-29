$(function () {
    function getCookie(c_name)
    {
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});


$( document ).ready(function(){


    //Preferences Page
    $('body').on('change', '#income_type', function(){
        var id = $('#income_type option:selected').val();
        var name = $('#income_type option:selected').html();

        if(name == "Hourly"){
            $('#salary_fields').addClass('hidden');
            $('#hourly_fields').removeClass('hidden');
        } else {
            $('#hourly_fields').addClass('hidden');
            $('#salary_fields').removeClass('hidden');
        }

        $('#apply_changes').removeClass('hidden');
    });

    $('body').on('input', "[id$='_income_amount']", function(){
        $('#apply_changes').removeClass('hidden');
    });

    $('body').on('click', '#apply_button', function(){
        var income_type_id = $('#income_type option:selected').val();
        var income_type_name = $('#income_type option:selected').html();
        var hourly_income = parseFloat($('#hourly_income_amount').val());
        var monthly_income = parseFloat($('#monthly_income_amount').val());

        var data = {
            action: "apply_changes",
            income_type_id: income_type_id
        };

        if(income_type_name == "Hourly"){
            if(hourly_income != NaN){
                data.hourly_income = hourly_income;
            } else {
                toastr.error("Hourly income must be a number");
                return;
            }
        } else {
            if(monthly_income != NaN){
                data.monthly_income = monthly_income;
            } else {
                toastr.error("Monthly income must be a number");
                return;
            }
        }

        $.ajax({
            url: "/preferences/",
            type: "POST",
            data: data,
            success: function(data, textStatus, jqXHR){
                toastr.success('Updated preferences');
                $('#hourly_income_amount').val(hourly_income.toFixed(2));
                $('#monthly_income_amount').val(monthly_income.toFixed(2));
                $('#apply_changes').addClass('hidden');
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error Updating Preferences")
            }
        });
    });

    $('#add_default_bill').autocomplete({
        source: '/api/v1/search_default_bill/',
        minLength: 0,
        select: function(event, ui){
            var name = $('#add_default_bill').val()
            $.ajax({
                url: '/api/v1/add_category/',
                type: 'POST',
                data: {
                    id: ui.item.id,
                    is_bill: 1,
                    is_default: 1,
                    name: name
                },
                success: function(data, textStatus, jqXHR){
                    if(data.success){
                        $('#default_bills_table tr:last').before(
                            '<tr id="category_' + data.id + '">' +
                                '<th>' + data.name + '</th>' +
                                '<th style="width:10%;">' +
                                    '<i id="delete_default_category_' + data.id + '" class="fa fa-trash fa-2 clickable"></i>' +
                                '</th>' +
                            '</tr>'
                        );
                        toastr.success("Added default bill");
                    } else {
                        toastr.error(name + " is already a default bill");
                    }
                    $('#add_default_bill').val("");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    $('#add_default_bill').val("");
                    toastr.error("Error adding default bill");
                }
            });
        }
    });

    $('#add_default_budget').autocomplete({
        source: '/api/v1/search_default_budget/',
        minLength: 0,
        select: function(event, ui){
            var name = $('#add_default_budget').val()
            $.ajax({
                url: '/api/v1/add_category/',
                type: 'POST',
                data: {
                    id: ui.item.id,
                    is_bill: 0,
                    is_default: 1,
                    name: name
                },
                success: function(data, textStatus, jqXHR){
                    if(data.success){
                        $('#default_budgets_table tr:last').before(
                            '<tr id="category_' + data.id + '">' +
                                '<th>' + data.name + '</th>' +
                                '<th style="width:10%;">' +
                                    '<i id="delete_default_category_' + data.id + '" class="fa fa-trash fa-2 clickable"></i>' +
                                '</th>' +
                            '</tr>'
                        );
                        toastr.success("Added default budget");
                    } else {
                        toastr.error(name + " is already a default budget");
                    }
                    $('#add_default_budget').val("");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    $('#add_default_bill').val("");
                    toastr.error("Error adding default bill");
                }
            });
        }
    });

    $('body').on('click', 'i[id^=delete_default_category]', function(){
        var element = $(this);
        var id = $(this).attr('id');
        id = id.substring(id.lastIndexOf("_")+1);

        $.ajax({
            url: "/api/v1/remove_default_category/",
            type: "POST",
            data: {id: id},
            success: function(data, textStatus, jqXHR){
                $('#category_' + id).fadeOut().remove();
                toastr.success("Removed default category");
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error removing default category");
            }
        });
    });
    //End Preferences Page

    //Dashboard Page
    $('body').on('click', '#general_button', function(){
        $('.active').removeClass('active');
        $(this).parent().addClass('active');
        $('#general_page').removeClass('hidden');
        $('#calendar_page').addClass('hidden');
        $('#expenses_page').addClass('hidden');
    });

    $('body').on('click', '#calendar_button', function(){
        $('.active').removeClass('active');
        $(this).parent().addClass('active');

        $('#calendar_page').removeClass('hidden');
        $('#general_page').addClass('hidden');
        $('#expenses_page').addClass('hidden');
    });

    $('body').on('click', '#expenses_button', function(){
        $('.active').removeClass('active');
        $(this).parent().addClass('active');

        $('#expenses_page').removeClass('hidden');
        $('#calendar_page').addClass('hidden');
        $('#general_page').addClass('hidden');
    });
    //End Dashboard Page


    $('#new_expense').click(function(){
        var now = new Date();
        var day = ("0" + now.getDate()).slice(-2);
        var month = ("0" + (now.getMonth() + 1)).slice(-2);

        $('#new_expense_date').val(now.getFullYear() + "-" + month + "-" +day);
    });

    $("button[id^=cancel_new_expense]").click(function(){
        $('#new_expense_amount').val("");
        $('#new_expense_description').val("");
        $('#new_expense_date').val("");
        $('#myModal').modal('toggle');
    });

    $('#submit_new_expense').click(function(){

        var success = true;

        if(success){
            toastr.success("Submitting new expense");
            $('#new_expense_amount').val("");
            $('#new_expense_description').val("");
            $('#new_expense_date').val("");
            $('#myModal').modal('toggle');
        } else {
            toastr.error("Error submitting new expense");
        }
    });




});