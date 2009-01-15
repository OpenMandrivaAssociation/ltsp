Name:           ltsp
Version:        5.1.44
Release:        %mkrel 1
Summary:        Linux Terminal Server Project Server and Client
Group:          Graphical desktop/Other

License:        GPLv2 and GPLv2+
URL:            http://www.ltsp.org
Source0:        ltsp-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: popt-devel
BuildRequires: popt
BuildRequires: flex bison
BuildRequires: automake
BuildRequires: pkgconfig
BuildRequires: libx11-devel
BuildRequires: syslinux
BuildRequires: tftp-server

%define _tftpdir /var/lib/tftpboot

%description
LTSP client and server

%package client
Summary:        LTSP client
Group:          Graphical desktop/Other
Requires:       chkconfig
Requires:       ltspfsd
Requires:       mille-xterm-nbd
Requires:       python-serial
BuildRequires:  glib2-devel

%description client
LTSP client package
This package contains the scripts necessary to boot as a LTSP5 thin client.

%package server
Summary:        LTSP server
Group:          System/Servers
Requires:       livecd-tools >= 015
Requires:       tftp-server
Requires:       ltspfs
Requires:       dhcp-server
Requires:       gettext
Requires:       bridge-utils
Requires:       nbd
Requires:       ldm

%description server
LTSP server package
This package contains the scripts and services necessary to install and run
a Linux Terminal Server.

%package vmclient
Summary:        LTSP Virtual Machine Client
Group:          Emulators
Requires:       kvm

%description vmclient
Run a qemu-kvm virtual machine as a PXE client.  This allows you to test a
LTSP server without the hassle of having extra hardware.  Requires
your system to support hardware virtualization or it will be very slow.

%prep
%setup -q

%build
pushd client/getltscfg
  %make
popd

pushd localapps
  %configure
  %make
popd


%install
rm -rf $RPM_BUILD_ROOT

# client
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/chroot-setup.d/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/template/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ldm/rc.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kernel/postinst.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kernel/prerm.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/

# server
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/kickstart/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/mkinitrd/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/scripts/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/scripts.d/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/chkconfig.d/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ltsp/swapfiles/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p $RPM_BUILD_ROOT/opt/ltsp
mkdir -p $RPM_BUILD_ROOT/opt/ltsp/images
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/cache/localapps/

mkdir -p $RPM_BUILD_ROOT%{_tftpdir}/ltsp/i386/pxelinux.cfg/
mkdir -p $RPM_BUILD_ROOT%{_tftpdir}/ltsp/x86_64/pxelinux.cfg/
mkdir -p $RPM_BUILD_ROOT%{_tftpdir}/ltsp/ppc/
mkdir -p $RPM_BUILD_ROOT%{_tftpdir}/ltsp/ppc64/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/live-config/

###### client install
pushd localapps
    make install DESTDIR=$RPM_BUILD_ROOT
popd
install -m 0755 localapps/ltsp-localappsd $RPM_BUILD_ROOT/%{_bindir}/

install -m 0755 client/getltscfg/getltscfg $RPM_BUILD_ROOT/%{_bindir}/getltscfg
install -m 0644 client/getltscfg/getltscfg.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
install -m 0644 client/ltsp_config $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0755 client/screen_session $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0755 client/configure-x.sh $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0644 client/initscripts/ltsp-init-common $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0644 ltsp-common-functions $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0755 client/initscripts/RPM/ltsp-client-launch $RPM_BUILD_ROOT%{_sbindir}
install -m 0644 client/rwtab.d/k12linux.rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d
install -m 0644 client/screen-x-common $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0755 client/xinitrc $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0755 client/jetpipe/jetpipe $RPM_BUILD_ROOT/%{_sbindir}
install -m 0644 client/jetpipe/jetpipe.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 0755 client/scripts/k12linux/ltsp-rewrap-latest-kernel $RPM_BUILD_ROOT/%{_sbindir}
install -m 0700 client/chroot-setup/ltsp-chroot-setup $RPM_BUILD_ROOT/%{_datadir}/ltsp/
install -m 0755 localapps/ldm-rc.d/S01-localapps $RPM_BUILD_ROOT%{_datadir}/ldm/rc.d/
cp -av client/chroot-setup/k12linux/* $RPM_BUILD_ROOT%{_datadir}/ltsp/chroot-setup.d/
cp -av client/screen.d $RPM_BUILD_ROOT/%{_datadir}/ltsp/
cp -av client/screen-session.d $RPM_BUILD_ROOT/%{_datadir}/ltsp/
cp -av client/xinitrc.d $RPM_BUILD_ROOT/%{_datadir}/ltsp/
cp -av client/template/k12linux/* $RPM_BUILD_ROOT%{_datadir}/ltsp/template/
touch $RPM_BUILD_ROOT%{_sysconfdir}/lts.conf
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/random-seed
# We need these files in both in client and server, but it ends up in the same place.
# client copy is to ensure that it gets upgraded with ltsp-client package upgrades.
# server copy is so chroot-creator can copy it into the chroot before mkinitrd runs the first time.
# the real client copy is written during ltsp-client %post iff it is actually a client chroot.
install -m 0644 server/configs/k12linux/mkinitrd/sysconfig-mkinitrd $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mkinitrd.ltsp-template
install -m 0755 server/configs/k12linux/mkinitrd/ltsp-postinst.d $RPM_BUILD_ROOT%{_sysconfdir}/kernel/postinst.d/ltsp
install -m 0755 server/configs/k12linux/mkinitrd/ltsp-prerm.d    $RPM_BUILD_ROOT%{_sysconfdir}/kernel/prerm.d/ltsp

### server install
install -m 0755 localapps/ltsp-localapps  $RPM_BUILD_ROOT/%{_bindir}/
install -m 0755 server/nbdrootd $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 server/nbdswapd $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 server/ltsp-update-sshkeys $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 server/ltsp-build-client $RPM_BUILD_ROOT%{_sbindir}
cp -pr server/plugins/* $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/
install -m 0755 server/ltsp-update-kernels $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 server/scripts/k12linux/ltsp-update-image $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 server/scripts/k12linux/chroot-creator $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 server/ltsp-swapfile-delete $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/
install -m 0644 server/xinetd.d/nbdrootd $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/
install -m 0644 server/xinetd.d/nbdswapd $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/
install -m 0644 server/configs/nbdswapd.conf $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/
cp -pr server/configs/kickstart/* $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/kickstart/
install -m 0644 server/configs/k12linux/mkinitrd/ifcfg-eth0 $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/mkinitrd/
install -m 0644 server/configs/k12linux/mkinitrd/sysconfig-mkinitrd $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/mkinitrd/
install -m 0644 server/configs/k12linux/mkinitrd/sysconfig-network $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/mkinitrd/
install -m 0755 server/configs/k12linux/mkinitrd/ltsp-postinst.d $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/mkinitrd/
install -m 0644 server/services/sysconfig-ltsp-dhcpd $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ltsp-dhcpd
install -m 0755 server/services/ltsp-dhcpd.init $RPM_BUILD_ROOT%{_sysconfdir}/init.d/ltsp-dhcpd
install -m 0755 server/scripts/k12linux/ltsp-prepare-kernel $RPM_BUILD_ROOT/%{_sbindir}/
install -m 0755 server/scripts/k12linux/ltsp-server-initialize $RPM_BUILD_ROOT/%{_sbindir}/
install -m 0755 server/scripts/k12linux/hosts-update $RPM_BUILD_ROOT/%{_datadir}/ltsp/scripts/
install -m 0755 server/scripts/k12linux/dhcpd-update $RPM_BUILD_ROOT/%{_datadir}/ltsp/scripts/
cp -p server/scripts/k12linux/scripts.d/*   $RPM_BUILD_ROOT%{_datadir}/ltsp/scripts.d/
cp -p server/scripts/k12linux/chkconfig.d/* $RPM_BUILD_ROOT%{_datadir}/ltsp/chkconfig.d/
cp -a server/configs/k12linux/live-config/* $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/live-config/
install -m 0644 server/scripts/k12linux/mksquashfs-exclude $RPM_BUILD_ROOT/%{_datadir}/ltsp/

# Remove irrelevant plugins from package
rm -rf $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/ltsp-build-client/ALTLinux/
rm -rf $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/ltsp-build-client/Debian/
rm -rf $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/ltsp-build-client/Gentoo/
rm -rf $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/ltsp-build-client/SUSE_LINUX/
rm -rf $RPM_BUILD_ROOT%{_datadir}/ltsp/plugins/ltsp-build-client/Ubuntu/

# configs
install -m 0644 server/configs/k12linux/ifcfg-ltspbr0 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
install -m 0644 server/configs/k12linux/ltsp-dhcpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/dhcpd.conf
install -m 0644 server/configs/k12linux/ltsp-update-kernels.conf $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/
install -m 0644 server/configs/k12linux/ltsp-build-client.conf $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/
install -m 0644 server/configs/k12linux/ltsp-server.conf $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/

for arch in i386 x86_64 ppc ppc64; do
    install -m 0644 server/configs/k12linux/lts.conf $RPM_BUILD_ROOT%{_tftpdir}/ltsp/$arch/
done

install -m 0644 server/configs/k12linux/ltspdist.template $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ltspdist

# PXE
install -m 0644 server/configs/pxe-default.conf $RPM_BUILD_ROOT%{_tftpdir}/ltsp/i386/pxelinux.cfg/default
install -m 0644 server/configs/pxe-default.conf $RPM_BUILD_ROOT%{_tftpdir}/ltsp/x86_64/pxelinux.cfg/default
install -m 0644 /usr/lib/syslinux/pxelinux.0 $RPM_BUILD_ROOT%{_tftpdir}/ltsp/i386
install -m 0644 /usr/lib/syslinux/pxelinux.0 $RPM_BUILD_ROOT%{_tftpdir}/ltsp/x86_64

# PPC
install -m 0644 server/configs/k12linux/yaboot-default.conf $RPM_BUILD_ROOT%{_tftpdir}/ltsp/ppc/yaboot.conf
install -m 0644 server/configs/k12linux/yaboot-default.conf $RPM_BUILD_ROOT%{_tftpdir}/ltsp/ppc64/yaboot.conf

# vmclient
install -m 0755 vmclient/ltsp-vmclient           $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 vmclient/ltsp-qemu-bridge-ifup   $RPM_BUILD_ROOT%{_sbindir}/
install -m 0644 vmclient/config-vmclient         $RPM_BUILD_ROOT%{_sysconfdir}/ltsp/vmclient

%clean
rm -rf $RPM_BUILD_ROOT

%post client
/usr/share/ltsp/ltsp-chroot-setup

%post server
/sbin/chkconfig --add ltsp-dhcpd

# If initial install, start the ltspbr0 bridge
# it would come up automatically in the next reboot.
if [ "$1" == "1" ]; then
    ifup ltspbr0 > /dev/null 2>&1 || :
fi

# During upgrades fix up config files
if [ $1 -gt 1 ]; then
    grep -q "flags" /etc/xinetd.d/nbdrootd
    [ $? -eq 1 ] && sed -i -e '/type  /a \\tflags\t\t= KEEPALIVE' /etc/xinetd.d/nbdrootd
    grep -q "flags" /etc/xinetd.d/nbdswapd
    [ $? -eq 1 ] && sed -i -e '/type  /a \\tflags\t\t= KEEPALIVE' /etc/xinetd.d/nbdswapd
    # Add server_args if missing from nbdrootd
    grep -q "server_args" /etc/xinetd.d/nbdrootd
    [ $? -eq 1 ] && sed -i -e '/server  /a \\tserver_args\t= /opt/ltsp/images/i386.img' /etc/xinetd.d/nbdrootd
    # Restart xinetd
    /sbin/service xinetd condrestart > /dev/null 2>&1
fi

%preun server
if [ $1 = 0 ]; then
    /sbin/service ltsp-dhcpd status >/dev/null 2>&1
    if [ $? = 3 ]; then
        /sbin/service ltsp-dhcpd stop >/dev/null 2>&1
    fi

    /sbin/chkconfig --del ltsp-dhcpd || :
    /sbin/service xinetd reload > /dev/null 2>&1 || :
fi

%postun server
if [ $1 -ge 1 ]; then
    /sbin/service ltsp-dhcpd condrestart >/dev/null 2>&1
fi

%files client
%defattr(-,root,root,-)
%{_mandir}/man1/getltscfg.1.lzma
%{_bindir}/getltscfg
%{_bindir}/xatomwait
%{_sbindir}/ltsp-client-launch
%dir %{_datadir}/ltsp
%{_datadir}/ltsp/configure-x.sh
%{_datadir}/ltsp/ltsp-init-common
%{_datadir}/ltsp/ltsp-common-functions
%{_datadir}/ltsp/ltsp_config
%{_datadir}/ltsp/screen_session
%{_datadir}/ltsp/screen-x-common
%{_datadir}/ltsp/screen.d/
%{_datadir}/ltsp/screen-session.d/
%{_datadir}/ltsp/xinitrc
%{_datadir}/ltsp/xinitrc.d/
%{_datadir}/ltsp/template/
%{_datadir}/ldm/rc.d/
%{_sbindir}/jetpipe
%{_sbindir}/ltsp-rewrap-latest-kernel
%{_mandir}/man8/jetpipe.8.lzma
%{_datadir}/ltsp/ltsp-chroot-setup
%{_datadir}/ltsp/chroot-setup.d/
%{_bindir}/ltsp-localappsd
%{_sysconfdir}/sysconfig/mkinitrd.ltsp-template
%{_sysconfdir}/kernel/postinst.d/ltsp
%{_sysconfdir}/kernel/prerm.d/ltsp

# readonly-root related files
%{_sysconfdir}/rwtab.d/*
%{_localstatedir}/lib/random-seed
%config(noreplace) %{_sysconfdir}/lts.conf

%files server
%defattr(-,root,root,-)
%doc ChangeLog COPYING TODO server/doc/lts-parameters.txt
%dir %{_localstatedir}/lib/ltsp/
%attr(700,nobody,nobody) %dir %{_localstatedir}/lib/ltsp/swapfiles/
%dir %{_tftpdir}/
%dir %{_tftpdir}/ltsp/
%dir %{_tftpdir}/ltsp/i386/
%dir %{_tftpdir}/ltsp/i386/pxelinux.cfg/
%dir %{_tftpdir}/ltsp/x86_64/
%dir %{_tftpdir}/ltsp/x86_64/pxelinux.cfg/
%dir %{_tftpdir}/ltsp/ppc/
%dir %{_tftpdir}/ltsp/ppc64/
%ifarch %{ix86} x86_64
%{_tftpdir}/ltsp/i386/pxelinux.0
%{_tftpdir}/ltsp/x86_64/pxelinux.0
%endif
%config(noreplace) %{_tftpdir}/ltsp/i386/pxelinux.cfg/default
%config(noreplace) %{_tftpdir}/ltsp/x86_64/pxelinux.cfg/default
%config(noreplace) %{_tftpdir}/ltsp/ppc/yaboot.conf
%config(noreplace) %{_tftpdir}/ltsp/ppc64/yaboot.conf
%{_bindir}/ltsp-localapps
%{_sysconfdir}/ltsp/live-config/

%dir /opt/ltsp
%dir /opt/ltsp/images

%{_sbindir}/ltsp-build-client
%{_datadir}/ltsp/plugins/
%{_sbindir}/ltsp-prepare-kernel
%{_sbindir}/ltsp-server-initialize
%{_sbindir}/ltsp-update-kernels
%{_sbindir}/ltsp-update-image
%{_datadir}/ltsp/scripts/
%{_datadir}/ltsp/scripts.d/
%{_datadir}/ltsp/chkconfig.d/
%{_datadir}/ltsp/mksquashfs-exclude
%{_datadir}/ltsp/ltsp-common-functions
%{_sbindir}/ltsp-update-sshkeys
%{_sbindir}/nbdrootd
%{_sbindir}/nbdswapd
%{_sbindir}/chroot-creator
%{_sysconfdir}/cron.daily/ltsp-swapfile-delete
%{_sysconfdir}/init.d/ltsp-dhcpd
%{_sysconfdir}/sysconfig/ltspdist
%config(noreplace) %{_sysconfdir}/xinetd.d/nbdrootd
%config(noreplace) %{_sysconfdir}/xinetd.d/nbdswapd
%dir %{_sysconfdir}/ltsp/
%dir %{_localstatedir}/cache/localapps/
# Configuration Files
%config(noreplace) %{_sysconfdir}/sysconfig/ltsp-dhcpd
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifcfg-ltspbr0
%config(noreplace) %{_sysconfdir}/ltsp/nbdswapd.conf
%config(noreplace) %{_sysconfdir}/ltsp/ltsp-build-client.conf
%config(noreplace) %{_sysconfdir}/ltsp/ltsp-server.conf
%config(noreplace) %{_sysconfdir}/ltsp/dhcpd.conf
%config(noreplace) %{_sysconfdir}/ltsp/ltsp-update-kernels.conf
%dir %{_sysconfdir}/ltsp/kickstart/
%dir %{_sysconfdir}/ltsp/kickstart/Fedora/
%{_sysconfdir}/ltsp/kickstart/Fedora/common.ks
%{_sysconfdir}/ltsp/kickstart/Fedora/common-i386.ks
%{_sysconfdir}/ltsp/kickstart/Fedora/common-ppc.ks
%{_sysconfdir}/ltsp/kickstart/Fedora/common-i686.ks
%{_sysconfdir}/ltsp/kickstart/Fedora/common-x86_64.ks
%dir %{_sysconfdir}/ltsp/kickstart/Fedora/9/
%{_sysconfdir}/ltsp/kickstart/*/*/*.ks
%dir %{_sysconfdir}/ltsp/mkinitrd/
%{_sysconfdir}/ltsp/mkinitrd/*
%config(noreplace) %{_tftpdir}/ltsp/*/lts.conf

%files vmclient
%defattr(-,root,root,-)
%{_sbindir}/ltsp-vmclient
%{_sbindir}/ltsp-qemu-bridge-ifup
%config(noreplace) %{_sysconfdir}/ltsp/vmclient
