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




    $('body').on('click', 'i[id^=delete_default_bill]', function(){
        var element = $(this);
        var id = $(this).attr('id');
        id = id.substring(id.lastIndexOf("_")+1);

        $.ajax({
            url: "/preferences/",
            type: "POST",
            data: {action: 'delete_default_bill', id: id},
            success: function(data, textStatus, jqXHR){
                $('#bill_' + id).remove();
                $('#add_default_bill').append(
                    '<option value="' + id +'">' + element.parent().text() + '</option>'
                );
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error removing default bill")
            }
        });
    });

    $('body').on('change', '#add_default_bill', function(){
        var selected = $(this).find(":selected");
        var id = selected.val();

        if(id == 0){
            return;
        }

        var name = selected.text();

        $.ajax({
            url: "/preferences/",
            type: "POST",
            data: {action: 'add_default_bill', id: id},
            success: function(data, textStatus, jqXHR){
                $('#default_bills_table').append(
                    '<tr id="bill_' + id + '"> <th>' + name + '<i id="delete_default_bill_' + id + '" class="fa fa-trash fa-2 trash"></i></th></tr>'
                );
                selected.remove();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error adding default bill")
            }
        });

    });


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