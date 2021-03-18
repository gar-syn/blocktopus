
// DataTable for Projects Page
$(document).ready(function() {

      function getCurrentSelectedLanguage() {
        var languageMap = {
            'en' : 'English',
            'de' : 'German',
            'fr' : 'French'
        }
        var lang = $('.selected-lang').attr('lang'); 
        return 'static/js/datatables-json/'+languageMap[lang]+'.json'
    }
    
  $('#table_projects').DataTable({
      language : {
          url: getCurrentSelectedLanguage()
        },
      "lengthChange": true,
      "bServerSide": true,
      "sPaginationType": "full_numbers",
      "iDisplayLength": 10,
      "stateSave": false,
      "sAjaxSource": "/load-projects",
      columns: [{
              data: 'id'
          },
          {
              data: 'title'
          },
          {
              data: 'description'
          },
          {
              data: 'created_date'
          },
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
      'columnDefs': [{
              'width': '25%',
              'targets': 2
          },
          {
              'width': '15%',
              'targets': 4
          }
      ],
      dom: 'Bfrtip',
      lengthMenu: [
          [10, 25, 50, -1],
          ['10 rows', '25 rows', '50 rows', 'All rows']
      ],
      buttons: {
          dom: {
              button: {
                  tag: 'button',
                  className: 'btn'
              }
          },
          buttons: [{
              extend: 'pageLength',
              className: 'btn-primary',
          }, {
              extend: 'copy',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3]
              }
          }, {
              extend: 'csv',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3]
              }
          }, {
              extend: 'excel',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3]
              }
          }, {
              extend: 'pdfHtml5',
              className: 'btn-outline-primary',
              orientation: 'landscape',
              pageSize: 'LEGAL',
              exportOptions: {
                  columns: [1, 2, 3, 4, 5, 6, 7]
              }
          }, {
              extend: 'print',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3]
              }
          }]
      },
      initComplete: function() {
          var api = this.api();
          api.column(0).visible(false);
      },
      drawCallback: function(settings) {
          $('[data-toggle="tooltip"]').tooltip();
      },
      rowCallback: function(row, data) {
          $(row).addClass(data.id);
      },
      createdRow: function(row, data, dataIndex) {
          $(row).find('td:eq(4) input')
              .attr('data-status', data.status ? 'locked' : 'unlocked')
              .addClass(data.id);
          $(row).find('td:eq(0)')
              .attr('data-status', data.status ? 'locked' : 'unlocked')
              .addClass(data.id);
      }
  });

  $('#table_projects').on('click', '.project-delete', function() {
      var project_guid = $(this).parents('tr').find("td:eq(0)").attr('class').split(' ')[0];
      var delete_project = Flask.url_for('forms.delete_project', {
          "id": project_guid
      });
      window.location.href = delete_project;
  })
  $('#table_projects').on('click', '.project-edit', function() {
      var project_guid = $(this).parents('tr').find("td:eq(0)").attr('class').split(' ')[0];
      var edit_project = Flask.url_for('forms.edit_project', {
          "id": project_guid
      });
      window.location.href = edit_project;
  })
  //Create Link for each row with Project GUID for experiments search
  $('#table_projects').on('click', 'tbody tr td:not(:last-child)', function() {
      var project_guid = $(this).parents('tr').find("td:eq(0)").attr('class').split(' ')[0];
      var filter_experiments_by_project_guid = Flask.url_for('queries.experiments', {
          "project-guid-filter": project_guid
      });
      window.location.href = filter_experiments_by_project_guid;
  });

  //Parse URL to get Project GUID for search query on experiments table
  function getExperimentsLinkedToProject(k) {
      if ($('table').is('#table_experiments') && (window.location.href.indexOf("project-guid-filter") > -1)) {
          var p = {};
          location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(s, k, v) {
              p[k] = v
          })
          return (k ? p[k] : p).split('%')[0];
      }
  }

  // DataTable for Experiments Page
  $('#table_experiments').DataTable({
    language : {
        url: getCurrentSelectedLanguage()
      },
      "oSearch": {
          "sSearch": getExperimentsLinkedToProject("project-guid-filter")
      },
      "lengthMenu": [
          [10, 25, 50, -1],
          [10, 25, 50, "All"]
      ],
      "lengthChange": true,
      "bServerSide": true,
      "sPaginationType": "full_numbers",
      "iDisplayLength": 10,
      "stateSave": false,
      "sAjaxSource": "/load-experiments",
      columns: [{
              data: 'id'
          },
          {
              data: 'eln'
          },
          {
              data: 'title'
          },
          {
              data: 'description'
          },
          {
              data: 'site'
          },
          {
              data: 'building'
          },
          {
              data: 'room'
          },
          {
              data: 'created_date'
          },
          {
              data: 'project_id'
          },
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
      'columnDefs': [{
          'width': '20%',
          'targets': 3
      }],
      dom: 'Bfrtip',
      lengthMenu: [
          [10, 25, 50, -1],
          ['10 rows', '25 rows', '50 rows', 'All rows']
      ],
      buttons: {
          dom: {
              button: {
                  tag: 'button',
                  className: 'btn'
              }
          },
          buttons: [{
              extend: 'pageLength',
              className: 'btn-primary',
          }, {
              extend: 'copy',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3, 4, 5, 6, 7]
              }
          }, {
              extend: 'csv',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3, 4, 5, 6, 7]
              }
          }, {
              extend: 'excel',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3, 4, 5, 6, 7]
              }
          }, {
              extend: 'pdfHtml5',
              className: 'btn-outline-primary',
              orientation: 'landscape',
              pageSize: 'LEGAL',
              exportOptions: {
                  columns: [1, 2, 3, 4, 5, 6, 7]
              }
          }, {
              extend: 'print',
              className: 'btn-outline-primary',
              exportOptions: {
                  columns: [1, 2, 3, 4, 5, 6, 7]
              }
          }]
      },
      initComplete: function() {
          var api = this.api();
          api.column(0).visible(false);
          api.column(8).visible(false);
      },
      drawCallback: function(settings) {
          $('[data-toggle="tooltip"]').tooltip();
      },
      rowCallback: function(row, data) {
          $(row).addClass(data.id);
      },
      createdRow: function(row, data, dataIndex) {
          $(row).find('td:eq(8) input')
              .attr('data-status', data.status ? 'locked' : 'unlocked')
              .addClass(data.id);
          $(row).find('td:eq(0)')
              .attr('data-status', data.status ? 'locked' : 'unlocked')
              .addClass(data.id);
      }
  });

  $('#table_experiments').on('click', '.experiment-delete', function() {
      var experiment_guid = $(this).parents('tr').attr('class').split(' ')[1];
      var delete_experiment = Flask.url_for('forms.delete_experiment', {
          "id": experiment_guid
      });
      window.location.href = delete_experiment;
  })
  $('#table_experiments').on('click', '.experiment-edit', function() {
      var experiment_guid = $(this).parents('tr').attr('class').split(' ')[1];
      var edit_experiment = Flask.url_for('forms.edit_experiment', {
          "id": experiment_guid
      });
      window.location.href = edit_experiment;
  })

  // DataTable to choose an Project for creating an Experiment
  $('#table_selection').DataTable({
    language : {
        url: getCurrentSelectedLanguage()
      },
      "lengthMenu": [
          [10, 25, 50, -1],
          [10, 25, 50, "All"]
      ],
      "lengthChange": true,
      "bServerSide": true,
      "sPaginationType": "full_numbers",
      "iDisplayLength": 10,
      "stateSave": true,
      "sAjaxSource": "/select-project",
      columns: [{
              data: 'id'
          },
          {
              data: 'title'
          },
          {
              data: 'description'
          },
          {
              data: 'created_date'
          },
          {
              "className": '',
              "orderable": false,
              "data": null,
              defaultContent: '<input type="button" class="btn btn-primary create-experiment" value="Create Experiment"/>'
          }
      ],
      initComplete: function() {
          var api = this.api();
          api.column(0).visible(false);
      },
      rowCallback: function(row, data) {
          $(row).addClass(data.id);
      },
      createdRow: function(row, data, dataIndex) {
          $(row).find('td:eq(0)')
              .attr('data-status', data.status ? 'locked' : 'unlocked')
              .addClass(data.id);
      }
  });

  // Project GUID via GET to the 'create experiment' form (foreign key)
  $('#table_selection').on('click', 'tbody tr', function() {
      var project_guid = $(this).attr('class').split(' ')[1];
      var create_experiment_url = Flask.url_for('forms.create_experiment', {
          "project-guid": project_guid
      });
      window.location.href = create_experiment_url;
  });
});