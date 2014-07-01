%global commit f0421d5ab0978bc0e293d2f9a09017aef2d23434
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:    freight
Version: 0.3.5
Release: 2%{?dist}
Summary: A modern take on the Debian archive

Group:   Development/Tools
License: BSD
URL:     https://github.com/rcrowley/freight
Source0: https://github.com/rcrowley/freight/archive/%{commit}/freight-%{commit}.tar.gz

BuildArch: noarch

Requires: coreutils
Requires: dpkg
Requires: gnupg

%description
freight programs create the files needed to serve a Debian archive. The actual
serving is done via your favorite HTTP server.

%prep
%setup -qn %{name}-%{commit}

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} \
             prefix=%{_prefix} \
             bindir=%{_bindir} \
             libdir=%{_datadir} \
             sysconfdir=%{_sysconfdir} \
             mandir=%{_mandir}

mv %{buildroot}/%{_sysconfdir}/freight.conf{.example,}

# VARLIB, freight library
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# VARCACHE, freight cache (to be served by httpd)
mkdir -p %{buildroot}%{_localstatedir}/cache/%{name}

# use /usr/share instead of /usr/lib for shell utils
find %{buildroot}%{_bindir} -type f -exec sed -i \
  '/dirname/ s|lib/freight|share/freight|g' {} +

%files
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_localstatedir}/cache/%{name}
%{_sharedstatedir}/%{name}
%{_sysconfdir}/bash_completion.d/%{name}
%{_sysconfdir}/profile.d/%{name}.sh
%config(noreplace) %{_sysconfdir}/%{name}.conf
%doc %{_mandir}

%changelog
* Tue Jul 01 2014 Dominic Cleal <dcleal@redhat.com> 0.3.5-2
- Remove /usr/lib symlink, edit bin scripts instead (dcleal@redhat.com)
- Fix formatting (dcleal@redhat.com)

* Tue Jul 01 2014 Dominic Cleal <dcleal@redhat.com> 0.3.5-1
- new package built with tito

