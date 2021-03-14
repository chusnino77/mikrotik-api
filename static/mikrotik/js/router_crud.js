$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-router .modal-content").html("");
                $("#modal-router").modal("show");
            },
            success: function (data) {
                $("#modal-router .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $(".router-list").html(data.html_router_list);
                    $("#modal-router").modal("hide");
                    toastr.success('Sccessfull !')
                }
                else {
                    $("#modal-router .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create router
    $(".js-create-router").click(loadForm);
    $("#modal-router").on("submit", ".js-router-create-form", saveForm);

    // Update router
    $(".router-list").on("click", ".js-update-router", loadForm);
    $("#modal-router").on("submit", ".js-router-update-form", saveForm);

    // Delete router
    $(".router-list").on("click", ".js-delete-router", loadForm);
    $("#modal-router").on("submit", ".js-router-delete-form", saveForm);

    // Test connections router
    $("#modal-router").on("click", ".btn-test", function () {
        $.get("/test-conn", $('.js-router-create-form').serialize(), function (data) {
            $('input[name="name"]').val(data.identity[0].name);
            $('input[name="routerboard"]').val(data.router[0].model);
            toastr.success('Connect successfull !') 
        }, "json").fail(function (jqXHR) {
            if (jqXHR.status == 500 || jqXHR.status == 0) {
                toastr.error('Failed to connect !')  
            }
        });
    });
});
