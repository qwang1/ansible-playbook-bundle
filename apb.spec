%if 0%{?fedora} || 0%{?rhel}
%global use_python3 0
%global use_python2 1
%global pythonbin %{__python2}
%global python_sitelib %{python2_sitelib}
%else
%else
%global use_python3 0
%global use_python2 1
%if 0%{?__python2:1}
%global pythonbin %{__python2}
%global python_sitelib %{python2_sitelib}
%else
%global pythonbin %{__python}
%global python_sitelib %{python_sitelib}
%endif
%endif
%{!?python_sitelib: %define python_sitelib %(%{pythonbin} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?copr}
%define build_timestamp .%(date +"%Y%m%d%H%M%%S")
%else
%define build_timestamp %{nil}
%endif

Name: apb
Version: 1.0.1
Release: 1%{build_timestamp}%{?dist}
Summary: Ansible Playbook Bundle (APB) is a lightweight application definition (meta-container).

Group: Development/Tools
License: GPLv2
URL: https://github.com/openshift/ansible-service-broker
Source0: https://github.com/ansibleplaybookbundle/ansible-playbook-bundle/archive/%{name}-%{version}.tar.gz

BuildArch: noarch
%if 0%{?use_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: python3-PyYAML >= 3.10
Requires: python3-PyYAML < 4
Requires: python3-docker >= 2.1.0
Requires: python3-docker < 3.0.0
Requires: python-openshift >= 1.0.0
Requires: python3-jinja2 >= 2.7.2
Requires: python3-requests >= 2.6.0
%else
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires: PyYAML >= 3.10
Requires: PyYAML < 4
Requires: python-docker >= 2.1.0
Requires: python-docker < 3.0.0
Requires: python-openshift >= 1.0.0
Requires: python-jinja2 >= 2.7.2
Requires: python-requests >= 2.6.0
%endif
Requires: docker

%description
Ansible Playbook Bundle (APB) is a lightweight application definition (meta-containers). APB
has the following features:

%package container-scripts
Summary: scripts required for running apb in a container
BuildArch: noarch
Requires: %{name}

%description container-scripts
containers scripts for apb

%prep
%setup -q -n %{name}-%{version}
sed -i '/req/d' setup.py

%build
%{pythonbin} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{pythonbin} setup.py install -O1 --skip-build --root %{buildroot}
install -d -m 755 %{buildroot}/%{_mandir}/man1/
cp docs/apb.1 %{buildroot}/%{_mandir}/man1/apb.1
install -d  %{buildroot}%{_bindir}
install -m 755 apb-wrapper %{buildroot}%{_bindir}/apb-wrapper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/apb
%dir %{python_sitelib}/apb
%{python_sitelib}/apb/*
%{python_sitelib}/apb-*.egg-info
%{_mandir}/man1/apb.1*

%files container-scripts
%{_bindir}/apb-wrapper

%changelog
* Thu Oct 12 2017 Jason Montleon <jmontleo@redhat.com> 1.0.1-1
- update the releasers (#139) (jmrodri@gmail.com)
- Document binding parameters and asynchronous bind. (#138) (cchase@redhat.com)
- Change broker_resource_url to fix apb relist. (#145) (derekwhatley@gmail.com)
- Fix pip install and errors when docker runs with a gid in use in the
  container (#141) (jmontleo@redhat.com)

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 1.0.0-1
- added key= to sorted call for Python 2.7.13 (#135) (cchase@redhat.com)
- Order services by name in apb list (#134) (karimboumedhel@gmail.com)
- Bug 1498613 - Add ability to specify Dockerfile name (#132)
  (dymurray@redhat.com)
- Bug 1498185 - Move version declaration into APB spec (#129)
  (dymurray@redhat.com)

* Wed Oct 04 2017 Jason Montleon <jmontleo@redhat.com> 0.2.5-1
- 1497819 - Remove image (#121) (david.j.zager@gmail.com)
- Changed setup.py URL and changed version in apb init (#128)
  (dymurray@redhat.com)
- Update to version 0.2.6 - pypi upload errors on 0.2.5 (dymurray@redhat.com)
- Bumping to 0.2.5-2 (dymurray@redhat.com)
- Update to 0.2.5 (dymurray@redhat.com)
- Added versioning explanation to developers.md (#127) (dymurray@redhat.com)
- [Proposal] Versioning of APBs (#117) (dymurray@redhat.com)
- Relist support (#124) (ernelson@redhat.com)
- fixing issue 125 (#126) (Shawn.Hurley21@gmail.com)
- adding ability to authenticate to the broker. (#123)
  (Shawn.Hurley21@gmail.com)
- This fixes issue-112. (#113) (Shawn.Hurley21@gmail.com)

* Tue Sep 19 2017 Jason Montleon <jmontleo@redhat.com> 0.2.4-1
- Update README.md (#114) (wmeng@redhat.com)
- Adding fix to apb tool to clean up on failed test pod run (#109)
  Shawn.Hurley21@gmail.com)
- Update display_type and display_group parameter docs to match UI (#106)
  (cfc@chasenc.com)
- Add APB testing to the apb tool (#104) (Shawn.Hurley21@gmail.com)
- Added unit testing setup and skeleton (#101) (jason.dobies@redhat.com)
- Fix alias command in README (#107) (jmontleo@redhat.com)

* Tue Aug 29 2017 Jason Montleon <jmontleo@redhat.com> 0.2.3-1
- new package built with tito

