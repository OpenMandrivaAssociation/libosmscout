# To verify the package works after an update:
# mkdir maps
# cd maps
# wget https://planet.osm.ch/switzerland-exact.osm.pbf
# Import switzerland-exact.osm.pbf --destinationDirectory . --typefile /usr/share/stylesheets/map.ost
# DrawMapQt `pwd` /usr/share/stylesheets/standard.oss 4096 8192 9.06 47.05 30000 test.png
# display test.png

%define major 0
%define beta %{nil}
%define scmrev 20180704
%define devname %mklibname -d osmscout

Name: libosmscout
Version: 0.0.1
# Code is from git://git.code.sf.net/p/libosmscout/code
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 3
Source0: %{name}-%{version}.tar.bz2
%else
Release: 0.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
#Patch1: libosmscout-opengl-linkage.patch
#Patch2:	libosmscout-build.sh-makeinstall.patch
#Patch4: libosmscout-label-contour-lines.patch
Summary: High-level interfaces to offline rendering and routing of OpenStreetMap data
URL: https://libosmscout.sf.net/
License: LGPL
Group: Sciences/Geosciences
Suggests: osmconvert

# libosmscout-import
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(zlib)

# libosmscout-map-qt
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)

# libosmscout-map-agg
BuildRequires: pkgconfig(libagg)

# libosmscout-map-opengl
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glu)
BuildRequires: pkgconfig(glut)

# libosmscout-map-svg
BuildRequires: pkgconfig(pango)
BuildRequires: pkgconfig(pangoft2)

# libosmscout-map-cairo
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(pangocairo)
BuildRequires: pkgconfig(libpng)

# OSMScout2
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Positioning)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: qmake5

%libpackage osmscout_client_qt 0
%libpackage osmscout_gpx 0
%libpackage osmscout_import 0
%libpackage osmscout_map_agg 0
%libpackage osmscout_map_cairo 0
%libpackage osmscout_map_qt 0
%libpackage osmscout_map 0
%libpackage osmscout_map_svg 0
%libpackage osmscout 0
%libpackage osmscout_test 0

%description
High-level interfaces to offline rendering and routing of OpenStreetMap data

%package import
Summary: OpenStreetMap data importer for %{name}
Group: Sciences/Geosciences
Requires: osmconvert

%description import
OpenStreetMap data importer for %{name}

%files import
%{_bindir}/Import
%{_bindir}/BasemapImport
%{_datadir}/%{name}

%package OSMScout
Summary: Sample map viewer for %{name}
Group: Sciences/Geosciences
Requires: qt5-qtpositioning

%description OSMScout
Sample map viewer for %{name}

%files OSMScout
%{_bindir}/OSMScout2
%dir %{_datadir}/osmscout
%doc %{_datadir}/osmscout/docs
%{_datadir}/stylesheets

%package StyleEditor
Summary: Map style editor for %{name}
Group: Sciences/Geosciences

%description StyleEditor
Map style editor for %{name}

%files StyleEditor

%package demos
Summary: Demo applications showing %{name}
Group: Sciences/Geosciences

%description demos
Demo applications showing %{name}

%files demos
%{_bindir}/Routing
%{_bindir}/RoutingAnimation
%{_bindir}/Navigation
%{_bindir}/Tiler
%{_bindir}/PerformanceTest
%{_bindir}/DrawMapQt
%{_bindir}/LocationDescription
%{_bindir}/LocationLookupForm
%{_bindir}/LocationLookup
%{_bindir}/POILookupForm
%{_bindir}/DumpData
%{_bindir}/ResourceConsumptionQt
%{_bindir}/DumpOSS
%{_bindir}/LookupPOI
%{_bindir}/DrawMapSVG
%{_bindir}/GpxPipe
%{_bindir}/ReverseLocationLookup
%{_bindir}/Coverage
%{_bindir}/DrawMapAgg
%{_bindir}/ResourceConsumption
%{_bindir}/DrawMapCairo

%package -n %{devname}
Summary: Development files for libosmscout
Group: Development/C
Requires: %{mklibname osmscout_client_qt 0} = %{EVRD}
Requires: %{mklibname osmscout_gpx 0} = %{EVRD}
Requires: %{mklibname osmscout_import 0} = %{EVRD}
Requires: %{mklibname osmscout_map_agg 0} = %{EVRD}
Requires: %{mklibname osmscout_map_cairo 0} = %{EVRD}
Requires: %{mklibname osmscout_map_qt 0} = %{EVRD}
Requires: %{mklibname osmscout_map 0} = %{EVRD}
Requires: %{mklibname osmscout_map_svg 0} = %{EVRD}
Requires: %{mklibname osmscout 0} = %{EVRD}
Requires: %{mklibname osmscout_test 0} = %{EVRD}

%description -n %{devname}
Development files for libosmscout

%files -n %{devname}
%{_includedir}/osmscout
%{_libdir}/*.so

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}
%endif
%autopatch -p1

%if 0
for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo libosmscout-client-qt Import OSMScout2 StyleEditor Demos Tests; do
	cd $i
	[ -e autogen.sh ] && ./autogen.sh
	if [ "$i" = "OSMScout2" -o "$i" = "StyleEditor" ]; then
		cat >res.qrc <<EOF
<!DOCTYPE RCC>
<RCC version="1.0">
<qresource prefix="/">
EOF
		find qml -type f |while read r; do
			echo "<file>$r</file>" >>res.qrc
		done
		echo '</qresource></RCC>' >>res.qrc
	fi
	if [ "$i" = "OSMScout2" ]; then
		sed -i -e 's,^ANDROID_EXTRA_LIBS.*=,LIBS +=,' *.pro
	fi
	if [ "$i" = "StyleEditor" ]; then
		echo 'RESOURCES += res.qrc' >>StyleEditor.pro
		sed -i -e 's,::fromLocalFile("qml/main.qml"),("qrc:/qml/main.qml"),g' src/MainWindow.cpp
cat >>StyleEditor.pro <<EOF
LIBS += ../libosmscout/src/.libs/libosmscout.so \
	../libosmscout-map/src/.libs//libosmscoutmap.so \
	../libosmscout-map-qt/src/.libs/libosmscoutmapqt.so
EOF
	fi
	cd ..
done
%else
%if "%{_lib}" != "lib"
find . -name CMakeLists.txt |xargs sed -i -e 's,DESTINATION lib,DESTINATION %{_lib},g'
%endif
find . -name CMakeLists.txt |xargs sed -i -e '/set_property(TARGET.*/iset_target_properties(${THE_TARGET_NAME} PROPERTIES VERSION %{version} SOVERSION 0)'
# Java bindings are disabled for now because of installation
# location weirdness. Should be fixed properly later.
%cmake \
	-DBUILD_IMPORT_TOOL_FOR_DISTRIBUTION:BOOL=ON \
	-DOSMSCOUT_BUILD_MAP_QT:BOOL=ON \
	-DOSMSCOUT_BUILD_BINDING_JAVA:BOOL=OFF \
%ifarch %{ix86} %{x86_64}
	-DOSMSCOUT_ENABLE_SSE:BOOL=ON \
%endif
	-G Ninja
%endif

%build
%if 0
for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo libosmscout-client-qt Import OSMScout2 StyleEditor Demos Tests; do
	cd $i
	if [ -e configure ]; then
		%configure
	else
		qmake-qt5 *.pro
	fi
	%make
	export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:$(pwd)
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/src/.libs
	cd ..
done
%else
%ninja_build -C build
%endif

%install
%if 0
cat >previous.list <<'EOF'
%dir 
%dir %{_prefix}
%dir %{_includedir}
%dir %{_libdir}
%dir %{_libdir}/pkgconfig
%dir %{_datadir}
%{_libdir}/pkgconfig
EOF
for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo libosmscout-client-qt Import OSMScout2 StyleEditor Demos Tests; do
	cd $i
	%makeinstall_std
	find %buildroot -name "*.la" |xargs rm -f
	cd ..
	( find %buildroot%{_includedir} -type d |sed -e 's,^%buildroot,%dir ,'; find %buildroot%{_includedir} -type f -o -type l |sed -e 's,^%buildroot,,'; find %buildroot -name "*.so" |sed -e 's,^%buildroot,,' ; find %buildroot%{_libdir}/pkgconfig |sed -e 's,^%buildroot,,' ; cat previous.list previous.list ) | sort | uniq -u >$i-devel.list
	( find %buildroot -type d |sed -e 's,^%buildroot,%dir ,'; find %buildroot -type f -o -type l |sed -e 's,^%buildroot,,' ; cat previous.list previous.list $i-devel.list $i-devel.list ) | sort | uniq -u >$i.list
	cat $i.list $i-devel.list >>previous.list
done

install -m 755 OSMScout2/debug/OSMScout %{buildroot}%{_bindir}/
install -m 755 StyleEditor/debug/StyleEditor %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a stylesheets %{buildroot}%{_datadir}/%{name}
cp -a maps %{buildroot}%{_datadir}/%{name}
%else
%ninja_install -C build
%endif

