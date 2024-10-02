// static/js/search.js
$(document).ready(function() {
    $('#txt-search').on('input', function() {
        let query = $(this).val();
        if (query.length > 2) {  // حداقل 3 کاراکتر باید وارد شود
            $.ajax({
                url: '/autocomplete_search/',
                data: {
                    'term': query
                },
                dataType: 'json',
                success: function(data) {
                    $('#suggestions').show();
                    $('#suggestions').empty();
                    $.each(data, function(index, item) {
                        $('#suggestions').append("<li style='border-bottom: 1px solid #ddd;'><i class='fa-solid fa-circle-check'></i> " + item.name + '</li>');
                    });

                    // اضافه کردن قابلیت کلیک روی هر آیتم
                    $('#suggestions li').on('click', function() {
                        $('#txt-search').val($(this).text());
                        $('#suggestions').empty();
                        $('#suggestions').hide();
                    });
                }
            });
        } else {
            $('#suggestions').empty();
            $('#suggestions').hide();
        }
    });
    });