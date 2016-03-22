$( document ).ready(function(){







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