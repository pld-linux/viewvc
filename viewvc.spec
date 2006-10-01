#
# TODO:	- release cgi, mod_python and, mayby admin part in subpackages
#	- mod_python configuration example in apache configuration snippet
#
Summary:	Browser interface for CVS and subversion version control repositories
#Summary(pl):
Name:		viewvc
Version:	1.0.2
Release:	0.1
License:	distributable
Group:		Applications/WWW
Source0:	http://viewvc.tigris.org/files/documents/3330/34450/%{name}-%{version}.tar.gz
# Source0-md5:	47569c8ab2ac67831340e460e685c3a9
URL:		http://www.viewvc.org/
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
%if %{with trigger}
Requires(triggerpostun):	sed >= 4.0
%endif
#Requires:	webserver(access)
#Requires:	webserver(alias)
#Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
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
 Support for filesystem-accessible CVS and Subversion repositories.
 Individually configurable virtual host support.
 Line-based annotation/blame display.
 Revision graph capabilities (via integration with CvsGraph) (CVS only).
 Syntax highlighting support (via integration with GNU enscript or Highlight).
 Bonsai-like repository query facilities.
 Template-driven output generation.
 Colorized, side-by-side differences.
 Tarball generation (by tag/branch for CVS, by revision for Subversion).
 I18N support based on the Accept-Language request header.
 Ability to run either as CGI script or as a standalone server.
 Regexp-based file searching.
 INI-like configuration file (as opposed to requiring actual code tweaks).

#%%description -l pl

%prep
%setup -q

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

# %webapp_* macros usage extracted from /usr/lib/rpm/macros.build:
#
# Usage:
#   %%webapp_register HTTPD WEBAPP
#   %%webapp_unregister HTTPD WEBAPP

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%if 00000000000000000000000000000000000
# SAMPLE TRIGGER FOR MIGRATION PURPOSES
%triggerpostun -- %{name} < 1.3.9-1.4
# rescue app configs. issue this in old config dir to get a list:
# rpm -qfl .|grep `pwd`/|awk -F/ '{print $NF}'|egrep -v 'apache|httpd'|xargs
for i in config.inc.php; do
	if [ -f /etc/%{name}/$i.rpmsave ]; then
		mv -f %{_webapps}/%{_webapp}/$i{,.rpmnew}
		mv -f /etc/%{name}/$i.rpmsave %{_webapps}/%{_webapp}/$i
	fi
done

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	httpd_reload=1
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
	httpd_reload=1
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_webapps}/%{_webapp}/apache.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_webapps}/%{_webapp}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
	fi
	rm -f /etc/%{name}/apache.conf.rpmsave
fi

# same but without separate %{_webapps}/%{_webapp} for package
if [ -f /etc/apache-%{name}.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_webapps}/%{_webapp}/apache.conf{,.rpmnew}
		cp -f /etc/apache-%{name}.conf.rpmsave %{_webapps}/%{_webapp}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
		cp -f /etc/apache-%{name}.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
	fi
	rm -f /etc/apache-%{name}.conf.rpmsave
fi

# update htpasswd path
#sed -i -e 's,/etc/%{name},%{_webapps}/%{_webapp},' %{_webapps}/%{_webapp}/{apache,httpd}.conf

# migrating from earlier apache-config?
if [ -L /etc/apache/conf.d/99_%{name}.conf ] || [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
		rm -f /etc/apache/conf.d/99_%{name}.conf
		apache_reload=1
	fi
	if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
		httpd_reload=1
	fi
else
	# no earlier registration. assume migration from Ra
	if [ -d /etc/apache/webapps.d ]; then
		apache_reload=1
	fi
	if [ -d /etc/httpd/webapps.d ]; then
		httpd_reload=1
	fi
fi

if [ "$apache_reload" ]; then
%{_sbindir}/webapp register apache %{_webapp}
	%service -q apache reload
fi
if [ "$httpd_reload" ]; then
%{_sbindir}/webapp register httpd %{_webapp}
	%service -q httpd reload
fi
%endif # END OF SAMPLE TRIGGER

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES COMMITTERS INSTALL TODO viewvc.org/license-1.html
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
#%%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%dir %{_appdir}/bin
%dir %{_appdir}/bin/cgi
%attr(750,root,http) %{_appdir}/bin/cgi/viewvc.cgi
%attr(750,root,http) %{_appdir}/bin/cgi/query.cgi
%dir %{_appdir}/bin/mod_python
%{_appdir}/bin/mod_python/viewvc.py
%{_appdir}/bin/mod_python/query.py
%{_appdir}/bin/mod_python/handler.py
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/bin/mod_python/.htaccess
%attr(750,root,http) %{_appdir}/bin/standalone.py
%attr(750,root,http) %{_appdir}/bin/loginfo-handler
%attr(750,root,http) %{_appdir}/bin/cvsdbadmin
%attr(750,root,http) %{_appdir}/bin/svndbadmin
%attr(750,root,http) %{_appdir}/bin/make-database
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
