#!/usr/bin/perl

use warnings;
use strict;

# based on https://stackoverflow.com/questions/303053/how-can-i-read-lines-from-the-end-of-file-in-perl
my ($file) = @ARGV;

my $filesize = -s $file;
my $offset = -2;
my $section = 0;
my %counties = ();
open F, $file or die "Can't read $file: $!\n";

# read the file backwards
while (abs($offset) < $filesize) {
    last if $section > 2;
    my $line = "";
    while (abs($offset) < $filesize) {
	seek F, $offset, 2;
	$offset -= 1;
	my $char = getc F;
	last if $char eq "\n";
	$line = $char . $line;
    }

    # parse each line
    $section++ if ($line =~ /%%/);
    my @data = split /:/, $line;
    if ($section == 1) {
	$counties{$data[0]} = $data[1];
    } else {
	$counties{$data[0]} -= $data[1];
    }
}

# based on https://perlmaven.com/highest-hash-value
my $count = 0;

while ($count < 10) {
    my $max;
    while(my ($county, $cases) = each %counties) {
	if (not defined $max) {
	    $max = $cases;
	    next;
	}
	if ($max < $cases) {
	    $max = $cases;
	}
    }

    if (defined $max) {
	while(my ($county, $cases) = each %counties) {
	    if ($cases == $max) {
		print "$county: $cases\n";
		delete $counties{$county};
	    }
	}
    }

    $count++;
}


