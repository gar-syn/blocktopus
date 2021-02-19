// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#table').DataTable({
    "lengthMenu": 15,
    "lengthChange": false,
    "bServerSide": true,
    "sPaginationType": "full_numbers",
    "iDisplayLength": 15,
    "sAjaxSource": "/load",
    columns:[
        {data: 'guid'},
        {data: 'title'},
        {data: 'description'},
        {data: 'created_date'}
    ]
})
});