%global commit f0421d5ab0978bc0e293d2f9a09017aef2d23434
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:    freight
Version: 0.3.5
Release: 1%{?dist}
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

# symlink /usr/lib/freight to /usr/share/freight as scripts expect it
mkdir -p %{buildroot}%{_prefix}/lib
ln -s %{_datadir}/%{name} %{buildroot}%{_prefix}/lib/%{name}

%files
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_localstatedir}/cache/%{name}
%{_sharedstatedir}/%{name}
%{_sysconfdir}/bash_completion.d/%{name}
%{_sysconfdir}/profile.d/%{name}.sh
%{_prefix}/lib/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%doc %{_mandir}

%changelog
* Tue Jul 01 2014 Dominic Cleal <dcleal@redhat.com> 0.3.5-1
- new package built with tito

