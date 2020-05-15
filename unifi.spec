# This is a binary package so debuginfo doesn't do anything useful.
%global debug_package %{nil}
%define __jar_repack %{nil}
%global __strip /bin/true

Name:           unifi
Version:        5.12.72
Release:        1%{?dist}
Summary:        Ubiquiti UniFi controller

License:        Proprietary
URL:            https://unifi-sdn.ubnt.com/

Source0:        http://dl.ui.com/unifi/%{version}/UniFi.unix.zip#/UniFi-%{version}.unix.zip
Source1:        unifi.service
Source2:        unifi.xml
Source3:        unifi-cloud.xml
Source4:        unifi.logrotate
Source6:        mongod.sh
Source100:      PERMISSION-1.html
Source101:      PERMISSION-2.html
Source102:      SETUP


BuildRequires:  systemd
%{?systemd_requires}
Requires(pre):  shadow-utils
Requires:       firewalld-filesystem
BuildRequires:  firewalld-filesystem
BuildRequires:  %{_bindir}/execstack

# https://fedoraproject.org/wiki/Changes/MongoDB_Removal
#Requires:       /usr/bin/mongod
Requires:       java-headless >= 1:1.8.0
Requires(post): policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils

# Unbundled fonts
Requires:       fontawesome-fonts
Requires:       fontawesome-fonts-web

# Prevent both packges from being installed.
Conflicts:      unifi-controller

# https://bugzilla.redhat.com/show_bug.cgi?id=1517565
Provides:       bundled(lato-fonts-web)
Provides:       bundled(ubnt-fonts)

# Bundled java ;obraries
# This needs to be automated!

Provides:       bundled(annotations) = 3.0.1
Provides:       bundled(aws-java-sdk-cloudwatch) = 1.11.409
Provides:       bundled(aws-java-sdk-core) = 1.11.409
Provides:       bundled(aws-java-sdk-s3) = 1.11.409
Provides:       bundled(commons-beanutils) = 1.9.3
Provides:       bundled(commons-codec) = 1.11
Provides:       bundled(commons-httpclient) = 3.1-2
Provides:       bundled(commons-httpclient-contrib) = 3.1
Provides:       bundled(commons-io) = 2.6
Provides:       bundled(commons-lang) = 2.6
Provides:       bundled(commons-logging) = 1.2
Provides:       bundled(commons-net) = 3.6
Provides:       bundled(commons-pool2) = 2.6.0
Provides:       bundled(commons-validator) = 1.6
Provides:       bundled(compiler) = 0.9.5
Provides:       bundled(cron4j) = 2.2.5
Provides:       bundled(dom4j) = 1.6.1
Provides:       bundled(ecj) = 4.6.1
Provides:       bundled(gson) = 2.8.5
Provides:       bundled(guava) = 26.0
Provides:       bundled(httpclient) = 4.5.6
Provides:       bundled(httpcore) = 4.4.10
Provides:       bundled(jackson-annotations) = 2.9.7
Provides:       bundled(jackson-core) = 2.9.7
Provides:       bundled(jackson-databind) = 2.9.7
Provides:       bundled(jedis) = 2.9.0
Provides:       bundled(jmdns) = 3.4.1
Provides:       bundled(joda-time) = 2.10.1
Provides:       bundled(jorbis) = 0.0.17
Provides:       bundled(jstl) = 1.2
Provides:       bundled(jstun) = 0.7.4
Provides:       bundled(jul-to-slf4j) = 1.7.25
Provides:       bundled(log4j) = 2.11.1
Provides:       bundled(mongo-java-driver) = 3.4.3
Provides:       bundled(radclient4)
Provides:       bundled(servo-core) = 0.12.25
Provides:       bundled(servo-graphite) = 0.12.25
Provides:       bundled(slf4j-api) = 1.7.25
Provides:       bundled(slf4j-log4j12) = 1.7.25
Provides:       bundled(snappy-java) = 1.1.7.2
Provides:       bundled(spring-beans) = 5.1.2
Provides:       bundled(spring-context) = 5.1.2
Provides:       bundled(spring-core) = 5.1.2
Provides:       bundled(spring-expression) = 5.1.2
Provides:       bundled(spring-test) = 5.1.2
Provides:       bundled(sshj) = 0.26.0
Provides:       bundled(tomcat-annotations-api) = 8.5.34
Provides:       bundled(tomcat-embed-core) =  8.5.34
Provides:       bundled(tomcat-embed-el) = 8.5.34
Provides:       bundled(tomcat-embed-jasper) = 8.5.34
Provides:       bundled(tomcat-embed-logging-juli) = 8.5.2
Provides:       bundled(tomcat-embed-logging-log4j) = 8.5.2
Provides:       bundled(urlrewritefilter) = 4.0.4

# So you can prevent automatic updates.
%if 0%{?fedora}
Recommends:     dnf-plugin-versionlock
%endif

Requires:       %{name}-data = %{version}-%{release}


%description
Ubiquiti UniFi server is a centralized management system for UniFi suite of
devices. After the UniFi server is installed, the UniFi controller can be
accessed on any web browser. The UniFi controller allows the operator to
instantly provision thousands of UniFi devices, map out network topology,
quickly manage system traffic, and further provision individual UniFi devices.


%package data
BuildArch:      noarch
Summary:        Non-architechture specific data files for unifi

%description data
Non-architechture specific data files for the unifi controller software.


%prep
%autosetup -n UniFi

install -pm 0644 %{SOURCE102} .

# Unbundle fontawesome fot
rm -f webapps/ROOT/app-unifi/fonts/*.{ttf,eot,otf,svg,woff,woff2}


%install
# Install into /usr/share/unifi
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a ./*  %{buildroot}%{_datadir}/%{name}/

# Remove readme as it will be handled by %%doc
rm -f %{buildroot}%{_datadir}/%{name}/readme.txt

### Attempt a more FHS compliant install...
# Create directories for live data and symlink it into /usr/share so unifi
# can find them.
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/{data,run,work}
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/data \
       %{buildroot}%{_datadir}/%{name}/data
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/run \
       %{buildroot}%{_datadir}/%{name}/run
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/work \
       %{buildroot}%{_datadir}/%{name}/work

# Create logs in /var/log and symlink it in.
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
ln -sr %{buildroot}%{_localstatedir}/log/%{name} \
       %{buildroot}%{_datadir}/%{name}/logs

# Install systemd service file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# Install firewalld config
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services
install -pm 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/firewalld/services/
install -pm 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/firewalld/services/

# Remove non-native executables
rm -rf %{buildroot}%{_datadir}/unifi/lib/native/{Windows,Mac}

# Bundled libs are only supported on x86_64, aarch64 and armv7hf.
# Move libraries to the correct location and symlink back
mv %{buildroot}%{_datadir}/unifi/lib/native/Linux ./
%ifarch x86_64 armv7hl aarch64
# Set the correct arch for the webrtc library.
%ifarch armv7hl
%global unifi_arch armv7
%else 
%global unifi_arch %{_target_cpu}
%endif
mkdir -p %{buildroot}%{_libdir}/unifi \
         %{buildroot}%{_datadir}/unifi/lib/native/Linux/%{unifi_arch}
install -pm 0755 Linux/%{unifi_arch}/*.so %{buildroot}%{_libdir}/%{name}/
for lib in $(ls %{buildroot}%{_libdir}/%{name}/*.so); do
    ln -sr $lib %{buildroot}%{_datadir}/unifi/lib/native/Linux/%{unifi_arch}
done

# Try to fix java VM warning about running execstack on libubnt_webrtc_jni.so
find %{buildroot}%{_libdir} -name libubnt_webrtc_jni.so -exec execstack -c {} \;
%endif

# Install logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install forum messages giving permission to redistribute.
install -p %{SOURCE100} %{SOURCE101} .

#
# Workaround script for MongoDB 3.6 no longer accepting --nohttpinterface.
# See: https://community.ubnt.com/t5/UniFi-Routing-Switching/MongoDB-3-6/m-p/2322445#M86254
#
install -pm 0755 %{SOURCE6} %{buildroot}%{_datadir}/unifi/bin/mongod

# Install sysconfig file.
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/%{name} <<EOL
# Add site specific java options here by assining "JAVA_OPTS"
EOL


%pre
getent group unifi >/dev/null || groupadd -r unifi
getent passwd unifi >/dev/null || \
    useradd -r -g unifi -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "Ubiquitu UniFi Controller" unifi
exit 0

%post
%systemd_post %{name}.service
%{?firewalld_reload}

# Set required SELinux context for unifi to use a private mongodb database.
%if "%{_selinux_policy_version}" != ""
    semanage fcontext -a -t mongod_log_t \
        "%{_localstatedir}/log/unifi(/.*)?" 2>/dev/null || :
    semanage fcontext -a -t mongod_var_lib_t \
        "%{_sharedstatedir}/unifi/data(/.*)?" 2>/dev/null || :
    restorecon -R %{_localstatedir}/log/unifi \
                  %{_sharedstatedir}/unifi/data || :
    semanage port -a -t mongod_port_t -p tcp 27117 2>/dev/null || :
%endif

%firewalld_reload


%preun
%systemd_preun %{name}.service

%postun
# Restart the service on upgrade.
%systemd_postun_with_restart %{name}.service
# Remove selinux modifications on uninstall
if [ $1 -eq 0 ] ; then  # final removal
%if "%{_selinux_policy_version}" != ""
    semanage fcontext -d -t mongod_log_t \
        "%{_localstatedir}/log/unifi(/.*)?" 2>/dev/null || :
    semanage fcontext -d -t mongod_var_lib_t \
        "%{_sharedstatedir}/unifi/data(/.*)?" 2>/dev/null || :
    semanage port -d -t mongod_port_t -p tcp 27117 2>/dev/null || :
%endif
fi


%files
%doc readme.txt SETUP
%license PERMISSION*.html
%ifarch x86_64 armv7hl aarch64
%{_libdir}/unifi/
%{_datadir}/unifi/lib/native/
%endif
%{_datadir}/unifi/bin/mongod
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_prefix}/lib/firewalld/services/*.xml
%ghost %attr(-,unifi,unifi) %config(missingok,noreplace) %{_sharedstatedir}/%{name}/data/system.properties
%attr(-,unifi,unifi) %{_localstatedir}/log/%{name}/
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/%{name}
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/%{name}/data
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/%{name}/run
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/%{name}/work

%files data
%exclude %{_datadir}/unifi/lib/native
%exclude %{_datadir}/unifi/bin/mongod
%{_datadir}/%{name}/


%changelog
* Fri May 15 2020 Alexander Jacocks <alexander@redhat.com> - 5.12.72-1
- Update to 5.12.72.

* Tue Mar 31 2020 Richard Shaw <hobbes1069@gmail.com> - 5.12.66-1
- Update to 5.12.66.

* Mon Mar 16 2020 Richard Shaw <hobbes1069@gmail.com> - 5.12.35-2
- Update java requires to work with change in java provides in Fedora.

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.12.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.35-1
- Update to 5.12.0.

* Thu Oct 10 2019 Richard Shaw <hobbes1069@gmail.com> - 5.11.46-3
- Remove mongod requires and move config info to SETUP.
- Fix Requires for java to comply with guidelines.
- Try JAVA_HOME instead of forcing java 1.8.0 via alternatives.

* Thu Oct 03 2019 Richard Shaw <hobbes1069@gmail.com> - 5.11.46-2
- Change requirement from policycoreutils-python to policycoreutils-python-utils
  so Python 3 is used instead of Python 2 to manage selinux contexts.

* Sun Sep 29 2019 Richard Shaw <hobbes1069@gmail.com> - 5.11.46-1
- Update to 5.11.46, for release notes see:
  https://community.ui.com/releases/UniFi-Network-Controller-5-11-46/1984aaf0-7243-4257-af83-70126714613e

* Wed Sep 11 2019 Richard Shaw <hobbes1069@gmail.com> - 5.11.39-1
- Update to 5.11.39.

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.10.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.25-1
- Update to 5.10.25.
- Remove obsolete shell script, unifi,sh.
- Remove --add-modules workaround as it does not apply to JRE 8 (OpenJDK 1.8.0).

* Sat Jun 01 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.24-1
- Update to 5.10.24.

* Wed May 29 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.23-2
- Require /usr/bin/mongod on F30+.

* Sat May 04 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.23-1
- Update to 5.10.23.

* Sun Apr 07 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.21-1
- Update to 5.10.21.

* Tue Mar 12 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.20-1
- Update to 5.10.20.

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.10.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Feb 26 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.19-1
- Update to 5.10.19

* Thu Feb 14 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.17-1
- Update to 5.10.17.

* Thu Feb 07 2019 Richard Shaw <hobbes1069@gmail.com> - 5.10.12-1
- Update to 5.10.12.

* Tue Nov 13 2018 Richard Shaw <hobbes1069@gmail.com> - 5.9.29-2
- Update systemd service file to deal with Java 10 in F29+, fixes BZ#5080.

* Thu Oct 04 2018 Richard Shaw <hobbes1069@gmail.com> - 5.9.29-1
- Update to 5.9.29, see:
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-SDN-Controller-5-9-29-Stable-has-been-released/ba-p/2516852

* Tue Sep 11 2018 Richard Shaw <hobbes1069@gmail.com> - 5.8.30-1
- Update to 5.8.30, see:
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-SDN-Controller-5-8-30-Stable-has-been-released/ba-p/2489957

* Wed Aug 22 2018 Richard Shaw <hobbes1069@gmail.com> - 5.8.28-1
- Update to 5.8.28

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.8.24-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 5.8.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Richard Shaw <hobbes1069@gmail.com> - 5.8.24-1
- Update to 5.8.24

* Sat Jun 30 2018 Richard Shaw <hobbes1069@gmail.com> - 5.8.23-1
- Update to 5.8.23.

* Mon May 07 2018 Richard Shaw <hobbes1069@gmail.com> - 5.7.23-2
- Add workaround shell script to prevent --nohttpdinterface from being passed to
  MongoDB.

* Tue Apr 17 2018 Richard Shaw <hobbes1069@gmail.com> - 5.7.23-1
- Update to 5.7.23.

* Thu Mar 08 2018 Richard Shaw <hobbes1069@gmail.com> - 5.7.20-1
- Update to 5.7.20.
- Add new webrtc target aarch64.

* Wed Feb 21 2018 Richard Shaw <hobbes1069@gmail.com> - 5.6.30-2
- Spec file cleanup.
- Add provides for bundled java libraries.

* Fri Jan 26 2018 Richard Shaw <hobbes1069@gmail.com> - 5.6.30-1
- Upate to latest upstream release.
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-5-6-30-Stable-has-been-released/ba-p/2220761

* Thu Jan 18 2018 Richard Shaw <hobbes1069@gmail.com> - 5.6.29-2
- Remove remaining bundled fontawesome fonts.
- Add requires for fontawesome-fonts and fontawesome-fonts-web.
- Fix URL.

* Tue Jan 02 2018 Richard Shaw <hobbes1069@gmail.com> - 5.6.29-1
- Update to latest upstream release.
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-5-6-29-Stable-has-been-released/ba-p/2191996

* Fri Dec 08 2017 Richard Shaw <hobbes1069@gmail.com> - 5.6.26-1
- Update to latest upstream release. For release notes see:
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-5-6-26-Stable-has-been-released/ba-p/2165432

* Tue Dec  5 2017 Richard Shaw <hobbes1069@gmail.com> - 5.6.22-2
- Only keep the binary we need per arch.
- Moved execstack to %%install.
- Unbundled Fontawesome font, added Provides for Lato fonts.
- Revert disabling of the auto dependency generator.
- Moved libubnt_webrtc_jni.so to %%{_libdir} and symlinked back to required
  location.
- Added recommends of dnf-plugin-versionlock on Fedora to prevent automatic
  upgrades.

* Sun Nov 19 2017 Richard Shaw <hobbes1069@gmail.com> - 5.6.22-1
- Update to latest upstream release.

* Mon Oct 30 2017 Richard Shaw <hobbes1069@gmail.com> - 5.5.24-1
- Update to latest upstream release.
- SystemD service file should now restart the controller when it exits
  normally, such as after restoring a backup.

* Sat Oct 28 2017 Richard Shaw <hobbes1069@gmail.com> - 5.5.20-5
- Drop SElinux policy requirement.

* Sat Sep 16 2017 Richard Shaw <hobbes1069@gmail.com> - 5.5.20-4
- Spec file cleanup per review request comments, RFBZ#4647.
- SELinux scripts now conditional if selinux policy is available.
- Removed nosrc option since it's no longer necessary.

* Fri Sep  8 2017 Richard Shaw <hobbes1069@gmail.com> - 5.5.20-3
- Add logrotate config.

* Wed Sep  6 2017 Richard Shaw <hobbes1069@gmail.com> - 5.5.20-2
- Fix log migration script.
- Add firewalld config for EL7 and Fedora.

* Mon Jul 31 2017 Richard Shaw <hobbes1069@gmail.com> - 5.5.20-1
- Update to latest upstream release.

* Sun Jun  4 2017 Richard Shaw <hobbes1069@gmail.com> - 5.4.16-1
- Update to latest upstream release.

* Wed Jan 25 2017 Richard Shaw <hobbes1069@gmail.com> - 5.4.9-1
- Update to latest upstream release.
- Release notes:
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-5-4-9-Stable-has-been-released/ba-p/1800599

* Tue Jan 24 2017 Richard Shaw <hobbes1069@gmail.com> - 5.3.8-2
- Work around problem with systemd/selinux confinement and noatsecure which
  prevents $ORIGIN from being evalueated in java's RPATH.
- Make UniFi log to the right directory.

* Sat Dec 31 2016 Richard Shaw <hobbes1069@gmail.com> - 5.3.8-1
- Update to latest upstream release.

* Sat Nov 12 2016 Richard Shaw <hobbes1069@gmail.com> - 5.2.9-1
- Update to latest upstream release.
  Full release notes:
  https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-5-2-9-is-released/ba-p/1694199

* Fri Aug 26 2016 Richard Shaw <hobbes1069@gmail.com> - 5.0.7-1
- Update to latest upstream release.

* Fri Aug 26 2016 Richard Shaw <hobbes1069@gmail.com> - 4.8.20-1
- Update to latest upstream release.

* Thu Apr 21 2016 Richard Shaw <hobbes1069@gmail.com> - 4.8.15-1
- Update to latest upstream release.

* Mon Feb 22 2016 Richard Shaw <hobbes1069@gmail.com> - 4.8.12-1
- Update to latest upstream release.

* Mon Jul 27 2015 Richard Shaw <hobbes1069@gmail.com> - 4.6.6-1
- Update to latest upstream release.
- Release notes: https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-4-6-6-is-released/ba-p/1288816

* Fri Jun 13 2014 Richard Shaw <hobbes1069@gmail.com> - 3.2.1-1
- Update to latest upstream release.

* Thu Feb  6 2014 Richard Shaw <hobbes1069@gmail.com> - 2.4.6-1
- Move to /usr/lib.
- Update systemd service file to run as non-root user unifi.
- Add selinux policy so it works with running selinux enforcing.

* Fri Jan 17 2014 George Machitidze <giomac@gmail.com>
- Initial build
