%define major 0
%define beta %{nil}
%define scmrev 20141223

Name: libosmscout
Version: 0.0.1
# Code is from git://git.code.sf.net/p/libosmscout/code
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 1
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
# Not part of libosmscout, but closely related to the importer
Source1: http://m.m.i24.cc/osmconvert.c
Patch0: libosmscout-fix-cxxflags-detection.patch
Patch1: libosmscout-opengl-linkage.patch
Patch2:	libosmscout-build.sh-makeinstall.patch
Summary: High-level interfaces to offline rendering and routing of OpenStreetMap data
URL: http://libosmscout.sf.net/
License: LGPL
Group: Sciences/Geosciences

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

%description
High-level interfaces to offline rendering and routing of OpenStreetMap data

%{expand:%(for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo; do
	N=`echo $i |sed -e 's,^lib,,;s,-,_,g'`
	echo "%%define ${N} %%mklibname $N %{major}"
	echo "%%define ${N}_devel %%mklibname -d $N"
	echo "%%package -n %%${N}"
	echo "Summary: $i, a part of %{name}"
	echo "Group: Sciences/Geosciences"
	echo "%%description -n %%${N}"
	echo "$i, a part of %{name}"
	echo "%%package -n %%${N}_devel"
	echo "Summary: Development files for $i, a part of %{name}"
	echo "%%description -n %%${N}_devel"
	echo "Development files for $i, a part of %{name}"
	echo "%%files -n %%${N} -f $i.list"
	echo "%%files -n %%${N}_devel -f $i-devel.list"
done)}

%package import
Summary: OpenStreetMap data importer for %{name}
Group: Sciences/Geosciences

%description import
OpenStreetMap data importer for %{name}

%files import
%{_bindir}/osmconvert
%{_bindir}/Import
%{_datadir}/%{name}

%package OSMScout
Summary: Sample map viewer for %{name}
Group: Sciences/Geosciences

%description OSMScout
Sample map viewer for %{name}

%files OSMScout
%{_bindir}/OSMScout

%package StyleEditor
Summary: Map style editor for %{name}
Group: Sciences/Geosciences

%description StyleEditor
Map style editor for %{name}

%files StyleEditor
%{_bindir}/StyleEditor

%package demos
Summary: Demo applications showing %{name}
Group: Sciences/Geosciences

%description demos
Demo applications showing %{name}

%files demos
%{_bindir}/CachePerformance
%{_bindir}/CalculateResolution
%{_bindir}/DrawMapAgg
%{_bindir}/DrawMapCairo
%{_bindir}/DrawMapOpenGL
%{_bindir}/DrawMapQt
%{_bindir}/DrawMapSVG
%{_bindir}/LocationLookup
%{_bindir}/LookupPOI
%{_bindir}/NumberSetPerformance
%{_bindir}/PerformanceTest
%{_bindir}/ReaderScannerPerformance
%{_bindir}/ResourceConsumption
%{_bindir}/ResourceConsumptionQt
%{_bindir}/ReverseLocationLookup
%{_bindir}/Routing
%{_bindir}/Srtm
%{_bindir}/Tiler

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}
%endif
%apply_patches

for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo Import OSMScout2 StyleEditor Demos Tests; do
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
	if [ "$i" = "StyleEditor" ]; then
		echo 'RESOURCES += res.qrc' >>StyleEditor.pro
		sed -i -e 's,::fromLocalFile("qml/main.qml"),("qrc:/qml/main.qml"),g' src/MainWindow.cpp
	fi
	cd ..
done

%build
for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo Import OSMScout2 StyleEditor Demos Tests; do
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
%__cc %{optflags} -o osmconvert %{SOURCE1} -lz

%install
cat >previous.list <<'EOF'
%dir 
%dir %{_prefix}
%dir %{_includedir}
%dir %{_libdir}
%dir %{_libdir}/pkgconfig
%dir %{_datadir}
%{_libdir}/pkgconfig
EOF
for i in libosmscout libosmscout-import libosmscout-map libosmscout-map-qt libosmscout-map-svg libosmscout-map-opengl libosmscout-map-agg libosmscout-map-cairo Import OSMScout2 StyleEditor Demos Tests; do
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

install -m 755 osmconvert %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a stylesheets %{buildroot}%{_datadir}/%{name}
cp -a maps %{buildroot}%{_datadir}/%{name}
