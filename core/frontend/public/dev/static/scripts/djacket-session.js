function highlight_codes () {
    $('.code-view pre').each(function (i, block) {
        hljs.highlightBlock(block);
    });
}


function setup_markdown () {
    var markdowns = [];

    marked.setOptions({
      renderer: new marked.Renderer(),
      gfm: true,
      tables: true,
      breaks: true,
      pedantic: false,
      sanitize: true,
      smartLists: true,
      smartypants: false
    });

    $('table#repo-content tbody tr td.repo-obj-name[type="blob"] a').each(function () {
        if ($(this).text().trim() == 'README.md' || $(this).text().trim() == 'README.rst') {
            markdowns.push($(this).attr('href'));
        }
    });

    if (markdowns.length > 0) {
        var file_name = markdowns[0].split('/')[markdowns[0].split('/').length-1];
        $.ajax({
            url: '/api' + markdowns[0].replace('.git/blob/', '.git/readme/'),
            type: 'get',
            success: function(data) {
                $('h2.markdown-title').html('<i class="fa fa-book"></i> ' + file_name);
                $('.markdown-preview .markdown-title').css('display', 'block');
                $('.markdown-preview .arrow-down').css('display', 'block');
                $('.markdown-preview .markdown-body').html(marked(data));
            },
            failure: function(data) {
                console.error('djacket > failed to get README file.');
            }
        });
    }
}


function process_dates () {
    $('.moment-date').each(function () {
        if (!$(this).hasClass('moment-dated')) {
            $(this).text(moment($(this).text()).fromNow());
            $(this).addClass('moment-dated');
        }
    });
}


function setup_pjax () {
    $(document).pjax('a[data-pjax]', '#pjax-container');

    $(document).on('pjax:start', function() {
        NProgress.start();
    });

    $(document).on('pjax:end', function() {
        NProgress.done();
    });
}


function setup_view_tabs () {
    jQuery('.pjax-tabs .tab-links a').on('click', function (e)  {
        var currentAttrValue = jQuery(this).attr('href');

        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
    });
}


function setup_static_tabs () {
    jQuery('.static-tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');

        // Show/Hide Tabs
        jQuery('.static-tabs ' + currentAttrValue).show().siblings().hide();

        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');

        e.preventDefault();
    });
}


function setup_nprogress() {
    NProgress.configure({ showSpinner: false });
}


function setup_file_icons () {
    $('i.obj-icon').each(function () {
        var obj_extention = $(this).attr('ext');
        $(this).addClass(get_icon(obj_extention)["icon"]);
    });
}


function _show_weekly_graphs (dataset) {
    var weekly_labels = ['Monday', 'Tuesday', 'Wednsday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    var weekly_datas = [];

    dataset = JSON.parse(dataset);
    for (data in dataset) {
        // weekly_labels.push(data);
        weekly_datas.push(dataset[data]);
    }

    var weekly_data = {
        labels: weekly_labels,
        datasets: [
            {
                label: "Weekly Commits",
                fillColor: "rgba(57,221,0,0.2)",
                strokeColor: "rgba(49,170,8,1)",
                pointColor: "rgba(26, 103, 0, 1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(20, 75, 1, 1)",
                data: weekly_datas
            }
        ]
    };

    var weekly_ctx = $("#repo-graphs #weekly-commits-graph").get(0).getContext("2d");
    var weekly_commits = new Chart(weekly_ctx).Line(weekly_data);
}


function _show_monthly_graphs (dataset) {
    var monthly_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                     'August', 'September', 'October', 'November', 'December'];
    var monthly_datas = [];

    dataset = JSON.parse(dataset);
    for (data in dataset) {
        // monthly_labels.push(data);
        monthly_datas.push(dataset[data]);
    }

    var monthly_data = {
        labels: monthly_labels,
        datasets: [
            {
                label: "Monthly Commits",
                fillColor: "rgba(57,221,0,0.2)",
                strokeColor: "rgba(49,170,8,1)",
                pointColor: "rgba(26, 103, 0, 1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(20, 75, 1, 1)",
                data: monthly_datas
            }
        ]
    };

    var monthly_ctx = $("#repo-graphs #monthly-commits-graph").get(0).getContext("2d");
    var monthly_commits = new Chart(monthly_ctx).Bar(monthly_data);
}


function show_graphs (dataset) {
    var weekly_dataset = JSON.parse('' + dataset + '')['weekly'];
    var monthly_dataset = JSON.parse('' + dataset + '')['monthly'];

    _show_weekly_graphs(weekly_dataset);
    _show_monthly_graphs(monthly_dataset);
}


function get_datasets () {
    var repo_graphs = $('#repo-graphs');
    if (repo_graphs.length) {
        $.ajax({
            url: '/api' + $('#repo-link').attr('href').trim() + '/commits_stats',
            type: 'get',
            success: function(data) {
                $('#graphs-loader').css('display', 'none');
                show_graphs(data);
            },
            failure: function(data) {
                console.error('djacket > failed to get repository graphs.');
            }
        });
    }
}


$(document).on('ready', function () {
    setup_nprogress();
    setup_view_tabs();
    setup_static_tabs();
    setup_pjax();
});


$(document).on('ready pjax:end', function () {
    highlight_codes();
    process_dates();
    setup_markdown();
    setup_file_icons();
    get_datasets();
});
