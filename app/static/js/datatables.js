// DataTable for Projects Page
$(document).ready(function() {
   $('#table_projects').DataTable({
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
        {data: 'created_date'},
        {
          "className": '',
          "orderable": false,
          "data": null,
          defaultContent: '<input type="button" class="project-edit btn btn-success" value="Edit"/> <input type="button" class="project-delete btn btn-danger" value="Delete"/>'
        }
    ],   
    rowCallback: function (row, data) {
            $(row).addClass(data.guid);
        },
        createdRow: function( row, data, dataIndex ) {
          // Set the data-status attribute, and add a class
          $( row ).find('td:eq(4) input')
              .attr('data-status', data.status ? 'locked' : 'unlocked')
              .addClass(data.guid);
            }
          });

$('#table_projects').on('click', '.project-delete', function() {
  var project_guid =$(this).parents('tr').find("td.sorting_1").html();
  var delete_project = Flask.url_for('forms.delete_project', {"id":project_guid});
  window.location.href = delete_project;
})
$('#table_projects').on('click', '.project-edit', function() {
  var project_guid =$(this).parents('tr').find("td.sorting_1").html();
  var edit_project = Flask.url_for('forms.edit_project', {"id":project_guid});
  window.location.href = edit_project;
})

// DataTable for Experiments Page
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

// DataTable to choose an Project for creating an Experiment
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
        "className": '',
        "orderable": false,
        "data": null,
        defaultContent: '<center><input type="button" class="btn btn-primary create-experiment" value="Create Experiment"/></center>'
      }
  ],   
  rowCallback: function (row, data) {
          $(row).addClass(data.guid);
      },
      createdRow: function( row, data, dataIndex ) {
        // Set the data-status attribute, and add a class
        $( row ).find('td:eq(0)')
            .attr('data-status', data.status ? 'locked' : 'unlocked')
            .addClass('project_guid');
    }

});

// Project GUID via GET to the 'create experiment' form (foreign key)
$('#table_selection').on('click', 'tbody tr', function(key) {
  var project_guid = $(this).find(".project_guid").html();
  var create_experiment_url = Flask.url_for('forms.create_experiment', {"project-guid":project_guid});
  window.location.href = create_experiment_url;
});
});

