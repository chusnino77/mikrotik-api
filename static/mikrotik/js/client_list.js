$(function () {
    if (sessionStorage.link_active) {
        $('#custom-tabs-one-tab').find(".nav-link").removeClass('active');
        $('#' + sessionStorage.link_active).addClass('active');
        $('#custom-tabs-one-tabContent').find('.tab-pane').removeClass('show active')
        $(sessionStorage.link_open).addClass('show active');
    }
    var setLink = function () {
        sessionStorage.link_active = $(this).attr('id');
        $('#custom-tabs-one-tab').find(".nav-link").removeClass('active');
        $(this).addClass('active');
        sessionStorage.link_open = $(this).attr('href');
        $('#custom-tabs-one-tabContent').find('.tab-pane').removeClass('show active')
        $($(this).attr('href')).addClass('show active');
    }
    $('#custom-tabs-one-home-tab').click(setLink);
    $('#custom-tabs-one-profile-tab').click(setLink);
    $('#custom-tabs-one-diff-tab').click(setLink);

    $('.client-list').DataTable({
        "responsive": true,
        "autoWidth": false,
    });
    $('.client-active').DataTable({
        "responsive": true,
        "autoWidth": false,
    });
    $('.client-nonactive').DataTable({
        "responsive": true,
        "autoWidth": false,
    });
    $("input[data-bootstrap-switch]").each(function () {
        $(this).bootstrapSwitch('state', $(this).prop('checked'));
    });
    // CRUD
    /* Functions */
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-client .modal-content").html("");
                $("#modal-client").modal("show");
            },
            success: function (data) {
                $("#modal-client .modal-content").html(data.html_form);
                if (btn.hasClass('js-update-client')) $('.js-client-update-form').attr('action', '/client-update/' + data.client.id)
                if (btn.hasClass('js-enable-client')){
                    $('#state').val(btn.attr('data-state'));
                    var text_question = 'Enable';
                    if(btn.attr('data-state') == 'false') text_question = 'Disable';
                    $('.question').text(text_question);
                } 
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
            statusCode: {
                500: function () {
                    toastr.error('secret with the same name already exists !')
                }
            },
            success: function (data) {
                if (data.form_is_valid) {
                    //Destroy the old Datatable
                    $('.client-list').DataTable().clear().destroy();
                    $(".client-list tbody").empty();
                    $(".client-list tbody").html(data.html_client_list);
                    $("#modal-client").modal("hide");
                    toastr.success('Sccessfull !')
                    //Create new Datatable
                    $('.client-list').DataTable({
                        "responsive": true,
                        "autoWidth": false,
                    });
                }
                else {
                    $("#modal-client .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };
    /* Binding */

    // Create client
    $(".js-create-client").click(loadForm);
    $("#modal-client").on("submit", ".js-client-create-form", saveForm);

    // Update client
    $(".client-list").on("click", ".js-update-client", loadForm);
    $("#modal-client").on("submit", ".js-client-update-form", saveForm);

    // Delete client
    $(".client-list").on("click", ".js-delete-client", loadForm);
    $("#modal-client").on("submit", ".js-client-delete-form", saveForm);
    
    // enabled client
    $(".client-list").on("click", ".js-enable-client", loadForm);
    $("#modal-client").on("submit", ".js-client-enable-form", saveForm);

    // ping client
    $(".client-active").on("click", ".js-ping-client", loadForm);
    $("#modal-client").on("submit", ".js-client-enable-form", saveForm);
});