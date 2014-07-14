# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       pcsc-lite

# >> macros
# << macros
%define upstream_build 3963

Summary:    PC/SC Lite smart card framework and applications
Version:    1.8.11
Release:    1
Group:      System/Libraries
License:    BSD
URL:        http://pcsclite.alioth.debian.org/
Source0:    https://alioth.debian.org/frs/download.php/file/%{upstream_build}/%{name}-%{version}.tar.bz2
Source1:    org.debian.pcsc-lite.policy
Source100:  pcsc-lite.yaml
Source101:  pcsc-lite-rpmlintrc
Patch0:     pcscd-1.8.10-safer-udev-usage.patch
Requires:   pcsc-ifd-handler
Requires(preun): systemd
Requires(post): systemd
Requires(post): /sbin/ldconfig
Requires(postun): systemd
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-backend-1)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  doxygen
BuildRequires:  perl
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  libtool

%description
The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
in a very small form factor for communicating to smartcards and
readers.  PC/SC Lite uses the same winscard API as used under
Windows(R).  This package includes the PC/SC Lite daemon, a resource
manager that coordinates communications with smart card readers and
smart cards that are connected to the system, as well as other command
line tools.


%package devel
Summary:    PC/SC Lite development files
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description devel
PC/SC Lite development files.


%package doc
Summary:    PC/SC Lite development files
Group:      Documentation
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}

%description doc
PC/SC Lite developer documentation.


%prep
%setup -q -n %{name}-1.8.10

# pcscd-1.8.10-safer-udev-usage.patch
%patch0 -p1
# >> setup
# Convert to utf-8
for file in ChangeLog; do
iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
touch -r $file $file.new && \
mv $file.new $file
done
# << setup

%build
# >> build pre
# << build pre

%configure --disable-static \
    --enable-polkit \
    --enable-usbdropdir=%{_libdir}/pcsc/drivers

make %{?_smp_mflags}

# >> build post
doxygen doc/doxygen.conf ; rm -f doc/api/*.{map,md5}
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
rm -f $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy

mkdir -p $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/

# Create empty directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pcscd

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Remove documentation installed in a wrong directory
rm -f $RPM_BUILD_ROOT%{_docdir}/pcsc-lite/README.DAEMON
# << install post

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
# >> post devel
/sbin/ldconfig
# << post devel

%postun devel
# >> postun devel
/sbin/ldconfig
# << postun devel

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog DRIVERS HELP README SECURITY TODO
%dir %{_sysconfdir}/reader.conf.d/
%{_unitdir}/pcscd.service
%{_unitdir}/pcscd.socket
%{_sbindir}/pcscd
%dir %{_libdir}/pcsc/
%dir %{_libdir}/pcsc/drivers/
%{_libdir}/libpcsclite.so.*
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/pcscd.8*
%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy
%ghost %dir %{_localstatedir}/run/pcscd/
# >> files
# << files

%files devel
%defattr(-,root,root,-)
%{_bindir}/pcsc-spy
%{_includedir}/PCSC/
%{_libdir}/libpcsclite.so
%{_libdir}/libpcscspy.so*
%{_libdir}/pkgconfig/libpcsclite.pc
%{_mandir}/man1/pcsc-spy.1*
# >> files devel
# << files devel

%files doc
%defattr(-,root,root,-)
%doc doc/api/ doc/example/pcsc_demo.c
# >> files doc
# << files doc
