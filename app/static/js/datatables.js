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
          defaultContent: `<button type="submit" class="btn btn-info project-edit table-buttons" data-toggle="tooltip" data-placement="bottom" title="Edit Project">
          <i class="far fa-edit fa-sm"></i>
          </button> 
          <button type="submit" class="btn btn-danger project-delete table-buttons" data-toggle="tooltip" data-placement="bottom" title="Delete Project"> 
          <i class="fas fa-trash fa-sm"></i>
          </button>`
        }
    ],
    drawCallback: function (settings) {
      $('[data-toggle="tooltip"]').tooltip();
    },   
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
      {
        "className": '',
        "orderable": false,
        "data": null,
        defaultContent: `<button type="submit" class="btn btn-info experiment-edit table-buttons"  data-toggle="tooltip" data-placement="bottom" title="Edit Experiment">
        <i class="far fa-edit fa-sm"></i>
        </button> 
        <button type="submit" class="btn btn-danger experiment-delete table-buttons" data-toggle="tooltip" data-placement="bottom" title="Delete Experiment"> 
        <i class="fas fa-trash fa-sm"></i>
        </button>`
      }
  ],
  drawCallback: function (settings) {
    $('[data-toggle="tooltip"]').tooltip();
  },    
  rowCallback: function (row, data) {
          $(row).addClass(data.guid);
      },
      createdRow: function( row, data, dataIndex ) {
        // Set the data-status attribute, and add a class
        $( row ).find('td:eq(8) input')
            .attr('data-status', data.status ? 'locked' : 'unlocked')
            .addClass(data.guid);
          }
        });
$('#table_experiments').on('click', '.experiment-delete', function() {
  var experiment_guid =$(this).parents('tr').find("td.sorting_1").html();
  var delete_experiment = Flask.url_for('forms.delete_experiment', {"id":experiment_guid});
  window.location.href = delete_experiment;
})
$('#table_experiments').on('click', '.experiment-edit', function() {
  var experiment_guid =$(this).parents('tr').find("td.sorting_1").html();
  var edit_experiment = Flask.url_for('forms.edit_experiment', {"id":experiment_guid});
  window.location.href = edit_experiment;
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
        defaultContent: '<input type="button" class="btn btn-primary create-experiment" value="Create Experiment"/>'
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

