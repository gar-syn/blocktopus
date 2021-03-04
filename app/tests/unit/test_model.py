import pytest

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, name, site, building and room
    """
    
    from ...models.model import User

    #Create User
    user = User('lastname@proivder.tld', 'SuperStrongPassword', 'Name', 'Site', 'Building', 'Room')
    assert user.email == 'lastname@proivder.tld'
    assert user.password == 'SuperStrongPassword'
    assert user.name == 'Name'
    assert user.site == 'Site'
    assert user.building == 'Building'
    assert user.room == 'Room'
    
def test_new_project():
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check the guid, title, description and creation date
    """    

    from ...models.model import Projects
    from ...views.forms import stringdate
    import uuid
    
    #Create Project
    project_guid = str(uuid.uuid4())
    date = stringdate()
    project = Projects(project_guid, 'Project Title', 'Project Description', date)
    assert project.guid == project_guid
    assert project.title == 'Project Title'
    assert project.description == 'Project Description'
    assert project.created_date == date
    
    
def test_new_experiment():
    """
    GIVEN a Experiment model
    WHEN a new Experiment is created
    THEN check the guid, eln, title, description, site, building, room, user, creation date, last edited date and project guid
    """
    
    from ...models.model import User, Projects, Experiments
    from ...views.forms import stringdate, stringdatetime
    import uuid
    
    #Create User
    user = User('lastname@proivder.tld', 'SuperStrongPassword', 'Name', 'Site', 'Building', 'Room')
    assert user.email == 'lastname@proivder.tld'
    assert user.password == 'SuperStrongPassword'
    assert user.name == 'Name'
    assert user.site == 'Site'
    assert user.building == 'Building'
    assert user.room == 'Room'
        
    #Create Project
    project_guid = str(uuid.uuid4())
    date = stringdate()
    last_changed_date = stringdatetime()
    project = Projects(project_guid, 'Project Title', 'Project Description', date)
    assert project.guid == project_guid
    assert project.title == 'Project Title'
    assert project.description == 'Project Description'
    assert project.created_date == date
        
    #Create Experiment
    experiment_guid = str(uuid.uuid4())
    experiment = Experiments(experiment_guid, 'ELN-NUMBER-00', 'Experiment Title', 'Experiment Description', user.site, user.building, user.room, user.name, date, last_changed_date, project.guid)
    assert experiment.guid == experiment_guid
    assert experiment.eln == 'ELN-NUMBER-00'
    assert experiment.title == 'Experiment Title'
    assert experiment.description == 'Experiment Description'
    assert experiment.site == user.site
    assert experiment.building == user.building
    assert experiment.room == user.room
    assert experiment.user_id == user.name
    assert experiment.created_date == date
    assert experiment.last_modified_date == last_changed_date
    assert experiment.project_guid == project.guid