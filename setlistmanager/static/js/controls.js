function detailFormatter(index, row) {
    var html = []
    $.each(row, function (key, value) {
      if (key!="id" && key!="metadata") {
      html.push('<div class="form-row"><div class="form-group col-md-6"><label for="input'
        + key + '">' + key + '</label>  <input type="text" class="form-control" id="input'
        + key + '" value="' + value + '"></div>')
      }
    })
    $('#details').html(html.join(''))
    return ''
  }