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


var TemplateController = {

    getTemplate: function (templateName) {
        $.get(config.TEMPLATES + templateName + '.html', function (template) {
            return template;
        });
    },
};

var ProjectController = {
    get: function (projectId) {
        ViewController.reset();

        if (!projectId) {
            $.getJSON(config.API + 'project', function (data) {
                var message = JSON.parse(data);

                template = TemplateController.getTemplate('projects');

                if (template && message.status === true) {
                    ViewController.set(Mustache.render(template, message.data));
                } else {
                    ViewController.set("", "", message.error);
                }
            })
            .fail(function(){
                ViewController.set("", "", "Could not reach API server");
            });
        } else {
            
        }
    },
};

$(document).ready(setupRoutes);