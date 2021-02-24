// Call the dataTables jQuery plugin
$(document).ready(function() {
  var table =  $('#table').DataTable({
    "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
    "lengthChange": true,
    "bServerSide": true,
    "sPaginationType": "full_numbers",
    "iDisplayLength": 10,
    "sAjaxSource": "/load-projects",
    columns:[
        {data: 'guid'},
        {data: 'title'},
        {data: 'description'},
        {data: 'created_date'}
    ]
})

$('#table_experiments').DataTable({
  "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
  "lengthChange": true,
  "bServerSide": true,
  "sPaginationType": "full_numbers",
  "iDisplayLength": 10,
  "sAjaxSource": "/load-experiments",
  columns:[
      {data: 'guid'},
      {data: 'eln'},
      {data: 'title'},
      {data: 'description'},
      {data: 'site'},
      {data: 'building'},
      {data: 'room'},
      {data: 'created_date'},
  ]
})

$('#table_selection').DataTable({
  "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
  "lengthChange": true,
  "bServerSide": true,
  "sPaginationType": "full_numbers",
  "iDisplayLength": 10,
  "sAjaxSource": "/select-project",
  columns:[
      {data: 'guid'},
      {data: 'title'},
      {data: 'description'},
      {data: 'created_date'},
      {
        defaultContent: '<center><input type="button" class="btn btn-primary create-experiment" value="Create Experiment"/></center>'
  
      }
  ],   
  rowCallback: function (row, data) {
          $(row).addClass(data.guid);
      }
});

$('#table_selection').on('click', 'tbody tr', function(key) {
  var classname = $(this).find(".sorting_1").html();
  var newURL = Flask.url_for('forms.create_experiment', {"id":classname});
  window.location.href = newURL;
});
});

