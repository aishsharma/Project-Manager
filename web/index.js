var config = {
    PAGES: './pages/',
    API: 'http://localhost:8080/api/',
    TEMPLATES: './templates/',
    COMPONENTS: './components/'
};

function setupRoutes() {
    // Routing Table
    var routes = {
        '': getPage('home'),
        'projects': ProjectController.get,
        'projects/:projectId': ProjectController.get,
    };

    //instantiating router
    var router = Router(routes);
    //Initialize router
    router.init();
}

function getPage(pageName) {
    $.get(config.PAGES + pageName + '.html', function (page) {
        ViewController.set(page);
    });
}

var ViewController = {
    reset: function () {
        $("#content").html('');
        $('#success').html('');
        $('#error').html('');
    },

    set: function (content, success, error) {
        if (content) {
            $("#content").html(content);
        }

        if (success) {
            $('#success').html(success);
        }

        if (error) {
            $('#error').html(error);
        }
    }
};

var ProjectController = {
    get: function (projectId) {
        ViewController.reset();

        if (!projectId) {
            console.log("Retreiving all projects data");
            $.getJSON(config.API + 'project', function (data) {

                console.log("Data retreived: " + data);

                var message = data;

                console.log("Message: " + message);

                var template = "";

                $.get(config.TEMPLATES + 'projects.html')
                    .done(function (template) {
                        if (template && message.status === true) {
                            console.log("Rendering template");
                            ViewController.set(Mustache.render(template, { "projects": message.data }));
                        } else {
                            console.log("There was an error somewhere");
                            ViewController.set("", "", message.error);
                        }
                    })
                    .fail(function () {
                        console.log("Could not retreive template");
                        $("#error").html("Could not retreive template");
                    });
            })
                .fail(function () {
                    ViewController.set("", "", "Could not reach API server");
                });
        } else {
            //Show tasks of specific project
            $.getJSON(config.API + "project/" + projectId)
                .done(function (data) {
                    var message = data;
                    var template = "";

                    $.get(config.TEMPLATES + 'project-tasks.html')
                        .done(function (template) {
                            if (template && message.status === true) {
                                console.log("Rendering template");
                                ViewController.set(Mustache.render(template, { "project": message.data, "tasks": message.data.tasks }));
                            } else {
                                console.log("There was an error somewhere");
                                ViewController.set("", "", message.error);
                            }
                        })
                        .fail(function () {
                            console.log("Could not retreive template");
                            $("#error").html("Could not retreive template");
                        });
                })
                .fail(function () {
                    ViewController.set("", "", "Could not reach API server");
                });
        }
    },
};

$(document).ready(setupRoutes);