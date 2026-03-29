#!/bin/bash

read -p "KURWEN SERIO CHCESZ ROZJEBAC MACIERZ??? [tn] " -r
[[ $REPLY =~ ^[YyTt]$ ]] || exit 1

echo "No dobra to teraz jeszcze tylko musisz byc rootem"

sudo -K
sudo  echo "Jestes rootem, teraz bedziesz mial przesrane" || exit 1

disks="/dev/sd[efghij]"
disks2="/dev/sdj /dev/sde /dev/sdi /dev/sdh /dev/sdg /dev/sdf"

sudo umount /dev/md8
sudo mdadm --stop /dev/md8

echo "Sprawdzam czy dyski nie sa zamontowane..."
mount | grep -q -e "$disks" && echo "Ktorys z dyskow jest zamontowany!!!" && exit 1
echo OK

echo "Sprawdzam czy dyski maja 3,7TB..."
for disk in $disks2 ; do
	disk=${disk/\/dev\//}
	lsblk -d -o "NAME,SIZE" | grep -qe "$disk.*3,7T" || (echo "Dysk $disk nie bangla" && exit 1)
done
echo OK

echo "Teraz upewnij sie, ze dyski $disks to sa te nalezace do zepsutej macierzy..."

gnome-disks

read -p "Wszystko OK? [tn] " -r
[[ $REPLY =~ ^[YyTt]$ ]] || exit 1

echo "Teraz nadpisze pierwsze sektory kazdego z dyskow (wszystkie twoje pornosy pojda wpizdu): $disks2"

read -p "Czy jestes absolutnie pewien ze nie chcesz ich wiecej ogladac? [tn] " -r
[[ $REPLY =~ ^[YyTt]$ ]] || exit 1

for disk in $disks2 ; do
	read -p "Rozpizgac dysk $disk? [tn] " -r
	[[ $REPLY =~ ^[YyTt]$ ]] || exit 1
	sudo dd if=/dev/zero of=$disk bs=512 count=8 || exit 1
	echo "Dysk $disk rozwalony. Teraz tworze od nowa tablice partycji"
	#sudo parted $disk mklabel gpt || exit 1
	#echo "Tablica partycji utworzona"
done

echo "Wszystkie dyski wyzerowane z nowa tablica partycji"
echo "Tworze macierz: $disks2"

sudo mdadm --create /dev/md8 --name tytan-storage --raid-devices=6 --level=5 --assume-clean $disks2 || exit 1

echo "Montuje macierz"
sudo mount /tytan/storage || exit 1

echo KONIEC.



