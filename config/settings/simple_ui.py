SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'
SIMPLEUI_INDEX = '#'
SIMPLEUI_LOGO = '/static/icons/LOGO.svg'
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menus': [
        {
            'name': 'О сайте',
            'icon': 'fa fa-database',
            'url': '/admin/about_us/siteinfo/'
        },
        {
            'name': 'Страницы',
            'icon': 'fa fa-book',
            'models': [
                {
                    'name': 'О нас',
                    'icon': 'fa fa-info-circle',
                    'models': [
                        {
                            'name': 'Страница О нас',
                            'icon': 'fa fa-file-text',
                            'url': '/admin/about_us/aboutpage/'
                        },
                        {
                            'name': 'Блоки',
                            'icon': 'fa fa-cubes',
                            'url': '/admin/about_us/contentblock/'
                        },
                    ]
                },
                {
                    'name': 'Портфолио',
                    'icon': 'fa fa-folder',
                    'models': [
                        {
                            'name': 'Страница Портфолио',
                            'icon': 'fa fa-file-text',
                            'url': '/admin/portfolio/portfoliopage/'
                        },
                        {
                            'name': 'Направление',
                            'icon': 'fa fa-arrows',
                            'url': '/admin/portfolio/portfolioduration/'
                        },
                        {
                            'name': 'Проекты',
                            'icon': 'fa fa-industry',
                            'url': '/admin/portfolio/portfolioproject/'
                        },
                    ]
                },
                {
                    'name': 'Услуги',
                    'icon': 'fa fa-user',
                    'models': [
                        {
                            'name': 'Страница Услуг',
                            'icon': 'fa fa-file-text',
                            'url': '/admin/services/servicepage/'
                        },
                        {
                            'name': 'Услуги',
                            'icon': 'fa fa-cube',
                            'url': '/admin/services/service/'
                        },
                        {
                            'name': 'Блоки сервисов',
                            'icon': 'fa fa-cubes',
                            'url': '/admin/services/contentblock/'
                        },
                    ]
                },
                {
                    'name': 'Контакты',
                    'icon': 'fa fa-address-book',
                    'url': '/admin/contacts/contact/'
                },
            ]
        },
        {
            'name': 'Заявки',
            'icon': 'fa fa-list',
            'url': '/admin/contacts/application/'
        },
    ]
}
