function displayConvertor (data) {
    tmp = '';
    if (data != 'None') {
        tmp = data;
    }
    return tmp;
}

$(document).ready(function(){

    $('.main.menu').visibility({
        type: 'fixed'
    });
    $('.overlay').visibility({
        type: 'fixed',
        offset: 80
    });

    $('.image').visibility({
        type: 'image',
        transition: 'vertical flip in',
        duration: 500
    });

    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });

    $('.main.menu .item').each(function(){
        $(this).click(function(){
            location.href = $(this).attr('href');
        });
    });

    $('.ui .dropdown').dropdown();
    // $('.ui .dropdown .assert-field').dropdown('set selected', 'Status Code');

    $('.ui.modal').modal({
        allowMultiple: true, 
    });

    // Preserve Templated URLs
    $.fn.api.settings.api = {
        'config add': '/config/add',
        'config remove': '/config/remove',
    };

    $('.remove_config').api({
      method : 'GET',
      action: 'config remove',
      beforeSend: function(settings) {
        var config_id = $(this).closest('td').attr('data-value');
        settings.data = {config_id: config_id};
        console.log(settings.data);
        return settings;
      },
      onSuccess: function(data) {
        if (data['code'] == 200) {
          var item = $(this).closest('tr');
          item.fadeTo("slow", 0.1, function() {
            $(this).slideUp(function() {
              $(this).remove();
            });
          });
        }
        else {
          alert('删除失败，请重试');
        }
      }
    });

    $('.parameter-add').click(function() {
        var cur_field = $(this).closest('.field');
        fields = cur_field.siblings('.parameters-row');
        if (fields.eq(0).css('display') === 'none') {
            fields.eq(0).show();
        } else {
            html = fields.eq(0).get(0).outerHTML;
            cur_field.before(html);
        }
    });

    $('.assert-add').click(function() {
        // var cur_field = $(this).closest('.field');
        // var table = cur_field.siblings('.assertions-table');
        // if (table.css('display') == 'none') {
        //     table.show();
        //     return
        // }
        // if ($('.asserts-row').length > 0) {
        //     last_tr = table.find('tr:eq(-1)');
        //     var html = last_tr.prop('outerHTML');
        //     console.log(html);
        //     last_tr.before(html);
        // }
        var cur_field = $(this).closest('.field');
        fields = cur_field.siblings('.asserts-row');
        if (fields.eq(0).css('display') === 'none') {
            fields.eq(0).show();
        } else {
            html = fields.eq(0).get(0).outerHTML;
            cur_field.before(html);
            $('.assert-comparison-dropdown').dropdown();
        }
    });

    $('.ui.form.config-add-form').form({
        fields: {
           app_name: {
              dentifier: 'app_name',
              rules: [
                  {
                      type   : 'empty',
                      prompt : '应用名称不能为空'
                  },
              ]
           },
           method: {
              dentifier: 'method',
              rules: [
                  {
                      type   : 'empty',
                      prompt : '请选择请求类型'
                  },
              ]
           },
        },
        onFailure: function() {
            return false;
        }
    })
    .api({
        method: 'POST',
        action: 'config add',
        serializeForm: true,
        data: $('.ui.form.config-add-form').serialize(),
        beforeSend: function(settings) {
            settings.data = $(this).serializeArray();
            var headers = Object();
            var parameters = Object();
            var asserts = new Array();
            for (i in settings.data) {
                var obj = settings.data[i];
                if (obj['name'] === 'parameter-value') {
                    if (settings.data[i-1]['value'] == "") {
                        continue;
                    }
                    key = settings.data[i-1]['value'];
                    value = obj['value'];
                    parameters[key] = value;
                }
                else if (obj['name'] === 'assert-value') {
                    var tmp = {};
                    if (settings.data[i-2]['value'] == "") {
                        continue;
                    }
                    tmp.assert_key = settings.data[i-2]['value'];
                    tmp.assert_comparison = settings.data[i-1]['value'];
                    tmp.assert_value = obj['value'];
                    asserts.push(tmp);
                }
            }
            // settings.data.push({'name': 'headers', 'value': JSON.stringify(headers)});
            if (parameters) {
                settings.data.push({'name': 'parameters', 'value': JSON.stringify(parameters)});
            }
            if (asserts.length != 0) {
                settings.data.push({'name': 'assertions', 'value': JSON.stringify(asserts)});
            }
            console.log(settings.data);
            return settings;
        },
        onSuccess: function(data) {
            console.log(data);
            $('.config-add-form-msg').text(data['msg']);
            if (data['code'] == 200) {
                $('.config-add-form-msg').removeClass('error').addClass('success');
            }
            else {
                $('.config-add-form-msg').removeClass('success').addClass('error');
                $('.config-add-form-msg').show();
            }
        }
    });

});
