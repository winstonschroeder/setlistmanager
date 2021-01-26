
    function songsDetailFormatter(index, row) {
        var html = []
        html.push('\
            <div class="card-body ms-5">\
            <h5 class="card-title"><b>Artist</b> '+row['composer_name'] + '</h5>\
            <h6 class="card-subtitle mb-2 text-muted"><b>Version</b> ' + row['version'] + '</h6>\
            </div>');
        return html.join('')
        }

    var $table = $('#songstable')
    $(function() {
        $('#bandselector').click(function () {
            $table.bootstrapTable('refresh')
        })
    })
  function queryParams() {
    var params = {}
    $('#songstoolbar').find('input[name]').each(function () {
      params[$(this).attr('name')] = $(this).val()
    })
    return params
  }
  function responseHandler(res) {
    return res.rows
  }


