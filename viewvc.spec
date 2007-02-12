Summary:	Browser interface for CVS and Subversion version control repositories
Summary(pl.UTF-8):	Interfejs przeglądarki do repozytoriów systemów kontroli wersji CVS i Subversion
Name:		viewvc
Version:	1.0.3
Release:	0.2
License:	BSD
Group:		Applications/WWW
Source0:	http://viewvc.tigris.org/files/documents/3330/34803/%{name}-%{version}.tar.gz
# Source0-md5:	3d44ad485d38bf9f61d8111661260b4a
URL:		http://www.viewvc.org/
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Obsoletes:	viewcvs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	/etc/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
ViewVC is a browser interface for CVS and Subversion version control
repositories. It generates templatized HTML to present navigable
directory, revision, and change log listings. It can display specific
versions of files as well as diffs between those versions. Basically,
ViewVC provides the bulk of the report-like functionality you expect
out of your version control tool, but much more prettily than the
average textual command-line program output.

Here are some of the additional features of ViewVC:
- Support for filesystem-accessible CVS and Subversion repositories.
- Individually configurable virtual host support.
- Line-based annotation/blame display.
- Revision graph capabilities (via integration with CvsGraph) (CVS
  only).
- Syntax highlighting support (via integration with GNU enscript or
  Highlight).
- Bonsai-like repository query facilities.
- Template-driven output generation.
- Colorized, side-by-side differences.
- Tarball generation (by tag/branch for CVS, by revision for
  Subversion).
- I18N support based on the Accept-Language request header.
- Ability to run either as CGI script or as a standalone server.
- Regexp-based file searching.
- INI-like configuration file (as opposed to requiring actual code
  tweaks).

In order to run viewvc you must install viewvc-cgi or
viewvc-mod_python package.

%description -l pl.UTF-8
ViewVC to interfejs przeglądarki do repozytoriów systemów kontroli
wersji CVS i Subversion. Generuje oparty o szablony HTML prezentujący
listingi katalogów, rewizji i historii zmian z możliwością nawigacji.
Może wyświetlać określone wersje plików oraz różnice między wersjami.
Zasadniczo ViewVC udostępnia sporą funkcjonalność generowania
raportów, jakiej można by oczekiwać od narzędzi do kontroli wersji,
ale daje ona dużo ładniejsze wyniki niż w przypadku narzędzi
działających z linii poleceń.

Niektóre dodatkowe możliwości ViewVC:
- obsługa repozytoriów CVS i Subversion dostępnych w systemie plików
- oddzielnie konfigurowalna obsługa wirtualnych hostów
- liniowe wyświetlanie przypisów/autorów ostatnich zmian
- możliwość rysowania wykresów rewizji (poprzez integrację z
  cvsgraphem - tylko CVS)
- obsługa podświetlania składni (poprzez integrację z GNU enscriptem
  lub Highlightem)
- uproszczenie zapytań w stylu Bonsai
- generowanie wyjścia w oparciu o szablony
- kolorowe, dwustronne różnice
- generowanie tarballi (po tagu/branchu w CVS-ie, po rewizji w
  Subversion)
- obsługa I18N w oparciu o nagłówek żądania Accept-Language
- możliwość uruchamiania jako skrypt CGI i samodzielny serwer
- wyszukiwanie plików w oparciu o wyrażenia regularne
- plik konfiguracyjny w stylu INI (nie wymagający modyfikacji kodu).

Aby uruchomić viewvc należy zainstalować pakiet viewvc-cgi lub
viewvc-mod_python.

%package cgi
Summary:	ViewVC - CGI interface
Summary(pl.UTF-8):	ViewVC - interfejs CGI
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	webserver(cgi)

%description cgi
ViewVC - CGI interface.

%description cgi -l pl.UTF-8
ViewVC - interfejs CGI.

%package mod_python
Summary:	ViewVC - mod_python interface
Summary(pl.UTF-8):	ViewVC - interfejs mod_python
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	apache-mod_python

%description mod_python
ViewVC - mod_python interface.

%description mod_python -l pl.UTF-8
ViewVC - interfejs mod_python.

%prep
%setup -q

# TODO: move to SourceX
cat > apache.conf <<'EOF'

<Directory %{_appdir}>
    AllowOverride None
    Allow from all
</Directory>

# Version1 (default): under /cgi-bin/viewvc.cgi address
ScriptAlias /cgi-bin/viewvc.cgi %{_appdir}/bin/cgi/viewvc.cgi
ScriptAlias /cgi-bin/viewvc-query.cgi %{_appdir}/bin/cgi/query.cgi

# if using apache2 mod_python:
# Alias /viewvc	%{_appdir}/bin/mod_python
# <Location /viewvc>
#    Allow from all
#	<IfModule mod_python.c>
#		AddHandler mod_python .py
#		PythonPath "sys.path+['%{_appdir}/bin/mod_python']"
#		PythonHandler handler
#		PythonDebug Off
#	</IfModule>
# </Location>

# Version 2: viewvc as handler to whole vhost:
#<VirtualHost *:80>
#   ServerName cvs
#
#   Alias /viewvc/ %{_appdir}
#   DocumentRoot %{_appdir}/bin/cgi/viewvc.cgi
#   <Location />
#       Options ExecCGI
#       Allow from all
#   </Location>
#</VirtualHost>

EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_webapps}/%{_webapp},%{_appdir},%{_sysconfdir}}

#install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
#install lighttpd.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/lighttpd.conf

./viewvc-install --destdir=$RPM_BUILD_ROOT --prefix=%{_appdir}

mv -f $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/cvsgraph.conf
mv -f $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/viewvc.conf
ln -sf %{_sysconfdir}/cvsgraph.conf $RPM_BUILD_ROOT%{_appdir}/cvsgraph.conf
ln -sf %{_sysconfdir}/viewvc.conf $RPM_BUILD_ROOT%{_appdir}/viewvc.conf

%py_postclean %{_appdir}/lib
rm -f $RPM_BUILD_ROOT%{_appdir}/lib/win32popen.pyc

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%if 0
%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}
%endif

%files
%defattr(644,root,root,755)
%doc CHANGES COMMITTERS INSTALL TODO viewvc.org/license-1.html
%dir %attr(755,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
#%%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%dir %{_appdir}
%dir %{_appdir}/bin
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/bin/mod_python/.htaccess
%attr(755,root,root) %{_appdir}/bin/standalone.py
%attr(755,root,root) %{_appdir}/bin/loginfo-handler
%attr(755,root,root) %{_appdir}/bin/cvsdbadmin
%attr(755,root,root) %{_appdir}/bin/svndbadmin
%attr(755,root,root) %{_appdir}/bin/make-database
%{_appdir}/viewvc.conf
%{_appdir}/cvsgraph.conf
%dir %{_appdir}/lib
%{_appdir}/lib/PyFontify.py[co]
%{_appdir}/lib/accept.py[co]
%{_appdir}/lib/blame.py[co]
%{_appdir}/lib/compat.py[co]
%{_appdir}/lib/compat_difflib.py[co]
%{_appdir}/lib/compat_ndiff.py[co]
%{_appdir}/lib/config.py[co]
%{_appdir}/lib/cvsdb.py[co]
%{_appdir}/lib/dbi.py[co]
%{_appdir}/lib/debug.py[co]
%{_appdir}/lib/ezt.py[co]
%{_appdir}/lib/idiff.py[co]
%{_appdir}/lib/popen.py[co]
%{_appdir}/lib/py2html.py[co]
%{_appdir}/lib/query.py[co]
%{_appdir}/lib/sapi.py[co]
%dir %{_appdir}/lib/vclib
%{_appdir}/lib/vclib/__init__.py[co]
%dir %{_appdir}/lib/vclib/bincvs
%{_appdir}/lib/vclib/bincvs/__init__.py[co]
%dir %{_appdir}/lib/vclib/ccvs
%{_appdir}/lib/vclib/ccvs/__init__.py[co]
%{_appdir}/lib/vclib/ccvs/blame.py[co]
%dir %{_appdir}/lib/vclib/ccvs/rcsparse
%{_appdir}/lib/vclib/ccvs/rcsparse/__init__.py[co]
%{_appdir}/lib/vclib/ccvs/rcsparse/common.py[co]
%{_appdir}/lib/vclib/ccvs/rcsparse/debug.py[co]
%{_appdir}/lib/vclib/ccvs/rcsparse/default.py[co]
%{_appdir}/lib/vclib/ccvs/rcsparse/texttools.py[co]
%dir %{_appdir}/lib/vclib/svn
%{_appdir}/lib/vclib/svn/__init__.py[co]
%dir %{_appdir}/lib/vclib/svn_ra
%{_appdir}/lib/vclib/svn_ra/__init__.py[co]
%{_appdir}/lib/viewvc.py[co]
%dir %{_appdir}/templates
%{_appdir}/templates/annotate.ezt
%{_appdir}/templates/diff.ezt
%{_appdir}/templates/dir_new.ezt
%{_appdir}/templates/directory.ezt
%dir %{_appdir}/templates/docroot
%{_appdir}/templates/docroot/help.css
%{_appdir}/templates/docroot/help_dirview.html
%{_appdir}/templates/docroot/help_log.html
%{_appdir}/templates/docroot/help_query.html
%{_appdir}/templates/docroot/help_rootview.html
%dir %{_appdir}/templates/docroot/images
%{_appdir}/templates/docroot/images/annotate.png
%{_appdir}/templates/docroot/images/back.png
%{_appdir}/templates/docroot/images/back_small.png
%{_appdir}/templates/docroot/images/broken.png
%{_appdir}/templates/docroot/images/chalk.jpg
%{_appdir}/templates/docroot/images/cvsgraph_16x16.png
%{_appdir}/templates/docroot/images/cvsgraph_32x32.png
%{_appdir}/templates/docroot/images/diff.png
%{_appdir}/templates/docroot/images/dir.png
%{_appdir}/templates/docroot/images/down.png
%{_appdir}/templates/docroot/images/download.png
%{_appdir}/templates/docroot/images/feed-icon-16x16.jpg
%{_appdir}/templates/docroot/images/forward.png
%{_appdir}/templates/docroot/images/list.png
%{_appdir}/templates/docroot/images/log.png
%{_appdir}/templates/docroot/images/logo.png
%{_appdir}/templates/docroot/images/text.png
%{_appdir}/templates/docroot/images/up.png
%{_appdir}/templates/docroot/images/view.png
%{_appdir}/templates/docroot/styles.css
%{_appdir}/templates/error.ezt
%{_appdir}/templates/graph.ezt
%dir %{_appdir}/templates/include
%{_appdir}/templates/include/diff_form.ezt
%{_appdir}/templates/include/dir_footer.ezt
%{_appdir}/templates/include/dir_header.ezt
%{_appdir}/templates/include/file_header.ezt
%{_appdir}/templates/include/footer.ezt
%{_appdir}/templates/include/header.ezt
%{_appdir}/templates/include/log_footer.ezt
%{_appdir}/templates/include/log_header.ezt
%{_appdir}/templates/include/paging.ezt
%{_appdir}/templates/include/pathrev_form.ezt
%{_appdir}/templates/include/sort.ezt
%{_appdir}/templates/log.ezt
%{_appdir}/templates/log_table.ezt
%{_appdir}/templates/markup.ezt
%{_appdir}/templates/query.ezt
%{_appdir}/templates/query_form.ezt
%{_appdir}/templates/query_results.ezt
%{_appdir}/templates/revision.ezt
%{_appdir}/templates/roots.ezt
%{_appdir}/templates/rss.ezt

%files cgi
%defattr(644,root,root,755)
%dir %{_appdir}/bin/cgi
%attr(755,root,root) %{_appdir}/bin/cgi/viewvc.cgi
%attr(755,root,root) %{_appdir}/bin/cgi/query.cgi

%files mod_python
%defattr(644,root,root,755)
%dir %{_appdir}/bin/mod_python
%{_appdir}/bin/mod_python/viewvc.py
%{_appdir}/bin/mod_python/query.py
%{_appdir}/bin/mod_python/handler.py
