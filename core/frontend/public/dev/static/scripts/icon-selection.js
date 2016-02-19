// icons and color of each file type.
icons = {
    "git": {
        "color": "",
        "icon": "devicons devicons-git"
    },
    "js": {
        "color": "",
        "icon": "devicons devicons-nodejs_small"
    },
    "css": {
        "color": "",
        "icon": "devicons devicons-css3"
    },
    "html": {
        "color": "",
        "icon": "devicons devicons-html5"
    },
    "java": {
        "color": "",
        "icon": "devicons devicons-java",
    },
    "rb": {
        "color": "",
        "icon": "devicons devicons-ruby"
    },
    "rails": {
        "color": "",
        "icon": "devicons devicons-ruby_on_rails"
    },
    "py": {
        "color": "",
        "icon": "devicons devicons-python",
    },
    "scala": {
        "color": "",
        "icon": "devicons devicons-scala"
    },
    "md": {
        "color": "",
        "icon": "devicons devicons-markdown",
    },
    "php": {
        "color": "",
        "icon": "devicons devicons-php"
    },
    "mysql": {
        "color": "",
        "icon": "devicons devicons-mysql"
    },
    "coffee": {
        "color": "",
        "icon": "devicons devicons-coffeescript"
    },
    "sass": {
        "color": "",
        "icon": "devicons devicons-sass"
    },
    "scss": {
        "color": "",
        "icon": "devicons devicons-sass"
    },
    "less": {
        "color": "",
        "icon": "devicons devicons-less"
    },
    "vs": {
        "color": "",
        "icon": "devicons devicons-visualstudio"
    },
    "sh": {
        "color": "",
        "icon": "devicons devicons-terminal"
    },
    "ps": {
        "color": "",
        "icon": "devicons devicons-photoshop"
    },
    "vim": {
        "color": "",
        "icon": "devicons devicons-vim"
    }
}

/*
    Returns an icon object for the given file type.
    'icon' object is of a format like this:
        icon = {
            "color": "somecolor",
            "icon": "someicon"
        }
 */
function get_icon (file_type) {
    // return an icon object.
    try {
        return {
            "color": icons[file_type].color,
            "icon": icons[file_type].icon
        }
    } catch (err) {
        return {
            "color": "",
            "icon": "fa fa-file-text-o"
        }
    }
}
