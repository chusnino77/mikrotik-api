$(function () {
    var setLink = function(){
        var id= this.id;
        if(id == 'nonaktif'){
            nav_link = 'custom-tabs-one-diff-tab';
            tab_open = '#custom-tabs-one-diff';
        }else if(id == 'aktif'){
            nav_link = 'custom-tabs-one-profile-tab';
            tab_open = '#custom-tabs-one-profile';
        }else{
            nav_link = 'custom-tabs-one-home-tab';
            tab_open = '#custom-tabs-one-home';
        }
        sessionStorage.link_active = nav_link;
        sessionStorage.link_open = tab_open;
    }
    $('#client').click(setLink);
    $('#aktif').click(setLink);
    $('#nonaktif').click(setLink);
});