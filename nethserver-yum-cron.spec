Summary: nethserver - configure yum-cron
%define name nethserver-yum-cron
Name: %{name}
%define version 0.1.4
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: yum-cron
Requires: perl-Email-Valid
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
configure yum-cron for automatic update

%changelog
* Fri Jun 23 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.1.4-1.ns7
- initial

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
/usr/bin/systemctl enable yum-cron
#/usr/bin/systemctl start  yum-cron

%postun
/usr/bin/systemctl disable yum-cron
/usr/bin/systemctl stop  yum-cron

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
