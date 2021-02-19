// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#table').DataTable({
    "lengthMenu": 10,
    "lengthChange": false,
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
  "lengthMenu": 10,
  "lengthChange": false,
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

});