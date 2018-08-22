#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys
import uuid


class ProjectCreator:
    BASE_PROJECT_URL = "https://github.com/arielcalzadadeveloper/django-base-project.git"

    def create(self, location):
        self._create_project(location)
        self._get_base_project(location)
        self._setup_environment_file(location)
        self._modify_wsgi_file(location)
        self._modify_urls_file(location)
        self._modify_settings_file(location)

    @staticmethod
    def _run_command(command, with_subprocess=True):
        """Run shell command"""
        print("Running command: {}".format(" ".join(command)))

        if with_subprocess:
            try:
                command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                process_output, _ = command_line_process.communicate()

                if command_line_process.returncode != 0:
                    raise Exception(process_output)
            except Exception as e:
                raise Exception(e)
        else:
            os.system(" ".join(command))

    def _create_project(self, location):
        command = [
            "django-admin",
            "startproject",
            "conf",
            location
        ]

        self._run_command(command)

    def _get_base_project(self, location):
        temporal_location = os.path.join(location, uuid.uuid4().hex)

        command = [
            "git",
            "clone",
            self.BASE_PROJECT_URL,
            temporal_location
        ]

        self._run_command(command)

        command = [
            "mv",
            "-f",
            "{}/*".format(temporal_location),
            location
        ]

        self._run_command(command, False)

        for file_name in [".yarnrc", ".gitignore"]:
            command = [
                "mv",
                "-f",
                os.path.join(temporal_location, file_name),
                location
            ]

            self._run_command(command, False)

        shutil.rmtree(temporal_location)

    def _setup_environment_file(self, location):
        # Rename example file
        source = os.path.join(location, "env.example")
        target = os.path.join(location, ".env")
        command = ["mv", "-f", source, target]
        self._run_command(command, False)

    def _modify_wsgi_file(self, location):
        path = os.path.join(location, "conf", "wsgi.py")

        with open(path, "r") as fh:
            contents = fh.read()

        old_string = "import os"
        new_string = "{}\nimport dotenv".format(old_string)
        contents = contents.replace(old_string, new_string)

        old_string = "from django.core.wsgi import get_wsgi_application"
        new_string = "{}\n\ndotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))".format(
            old_string)
        contents = contents.replace(old_string, new_string)

        with open(path, "w") as fh:
            fh.write(contents)

    def _modify_urls_file(self, location):
        path = os.path.join(location, "conf", "urls.py")

        with open(path, "r") as fh:
            contents = fh.read()

        # Add django imports
        new_imports = [
            "from django.conf import settings",
        ]
        old_string = "from django.urls import path"
        new_string = "{}\n{}".format(old_string, "\n".join(new_imports))
        contents = contents.replace(old_string, new_string)

        # Add imports
        new_imports = [
            "import allauth",
            "import dynamic_raw_id",
        ]
        old_string = "from django.conf import settings"
        new_string = "{}\n\n{}".format(old_string, "\n".join(new_imports))
        contents = contents.replace(old_string, new_string)

        # Add patterns
        new_patterns = [
            "    path('accounts/', allauth.urls),",
            "    path('admin/dynamic_raw_id/', dynamic_raw_id.urls),",
        ]
        old_string = "    path('admin/', admin.site.urls),"
        new_string = "{}\n\n{}".format(old_string, "\n".join(new_patterns))
        contents = contents.replace(old_string, new_string)

        # Add media access if DEBUG
        contents += "\n"
        contents += "if settings.DEBUG:\n"
        contents += "    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"

        # Add admin titles
        contents += "\n\n"
        contents += "admin.site.site_header = 'Base Project'\n"
        contents += "admin.site.index_header = 'Base Project'"

        with open(path, "w") as fh:
            fh.write(contents)

    def _modify_settings_file(self, location):
        path = os.path.join(location, "conf", "settings.py")

        with open(path, "r") as fh:
            contents = fh.read()

        # DEBUG
        old_string = "DEBUG = True"
        new_string = "{}\nTrue if os.getenv('DEBUG') == 'True' else False".format(old_string)
        contents = contents.replace(old_string, new_string)

        # Allowed hosts
        old_string = "ALLOWED_HOSTS = []"
        new_string = "ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')".format(old_string)
        contents = contents.replace(old_string, new_string)

        # Installed apps
        new_applications = [
            "'django.contrib.sites',",
            "'django.contrib.humanize',",
            '',
            "'crispy_forms',",
            '',
            "'applications.common',",
            "'applications.users',",
            '',
            "'allauth',",
            "'allauth.account',",
            "'allauth.socialaccount',",
            "'dynamic_raw_id',",
            '',
            "'applications.last_app',",
        ]
        old_string = "'django.contrib.staticfiles',"
        new_string = "{}\n\n    {}".format(old_string, "\n    ".join(new_applications))
        contents = contents.replace(old_string, new_string)

        # Templates
        old_string = "'django.contrib.messages.context_processors.messages',"
        new_string = "{}\n\n{}{}".format(old_string, "    " * 4, "'applications.common.context_processors.general',")
        contents = contents.replace(old_string, new_string)

        old_string = "WSGI_APPLICATION = 'conf.wsgi.application'"
        new_builtins_list = "['django.templatetags.static', 'crispy_forms.templatetags.crispy_forms_tags']"
        new_builtins = """TEMPLATES[0]["OPTIONS"]["builtins"] = {}""".format(new_builtins_list)
        new_string = "{}\n\n{}".format(new_builtins, old_string)
        contents = contents.replace(old_string, new_string)

        # Authentication backends
        old_string = "WSGI_APPLICATION = 'conf.wsgi.application'"
        backends = "'django.contrib.auth.backends.ModelBackend',"
        backends += "\n{}'allauth.account.auth_backends.AuthenticationBackend'".format(" " * 27)
        auth_backends = """AUTHENTICATION_BACKENDS = ({},)""".format(backends)
        new_string = "{}\n\n{}".format(old_string, auth_backends)
        contents = contents.replace(old_string, new_string)

        # All auth
        old_string = "# Database"
        allauth_options = """# All auth
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = reverse_lazy("home")
ACCOUNT_ADAPTER = "applications.users.account_adapter.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[ST] "
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_EMAIL_MAX_LENGTH = 254
ACCOUNT_FORMS = {}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy("account_login")
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_PRESERVE_USERNAME_CASING = True
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_SIGNUP_FORM_CLASS = None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_TEMPLATE_EXTENSION = "html"
ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USERNAME_VALIDATORS = None
        """
        new_string = "{}\n\n{}".format(allauth_options, old_string)
        contents = contents.replace(old_string, new_string)

        # Database
        old_string = """'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),"""
        new_string = """'NAME': os.path.join(BASE_DIR, 'db', os.getenv("DB_NAME")) if 'sqlite3' in os.getenv("DB_ENGINE") else os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),"""
        contents = contents.replace(old_string, new_string)

        old_string = """'ENGINE': 'django.db.backends.sqlite3',"""
        new_string = """'ENGINE': os.getenv("DB_ENGINE"),"""
        contents = contents.replace(old_string, new_string)

        # Internationalization
        old_string = """LANGUAGE_CODE = 'en-us'"""
        new_string = """LANGUAGE_CODE = 'es-co'"""
        contents = contents.replace(old_string, new_string)

        old_string = """TIME_ZONE = 'UTC'"""
        new_string = """TIME_ZONE = 'America/Bogota'"""
        contents = contents.replace(old_string, new_string)

        # Static/Media files
        old_string = "STATIC_URL = '/static/'"
        new_string = """STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_URL = "/base_project_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/base_project_media/"""
        contents = contents.replace(old_string, new_string)

        # Last sections
        contents += """
# Allow thousand separator
USE_THOUSAND_SEPARATOR = True

# Crispy forms
CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_FAIL_SILENTLY = not DEBUG

# Browser window title
BROWSER_WINDOW_TITLE = "Base project"
"""
        with open(path, "w") as fh:
            fh.write(contents)


def main():
    parser = argparse.ArgumentParser(description="Creates a Django Project")
    parser.add_argument('location', help='Location for the new project, this must not exist.')

    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.location):
        os.makedirs(args.location)

    creator = ProjectCreator()
    creator.create(args.location)


if __name__ == "__main__":
    main()
