#!/usr/bin/env perl
# A script to calculate N50 from one or multiple FASTA/FASTQ files, 
# or from STDIN.

use v5.12;
use Pod::Usage;
use Term::ANSIColor  qw(:constants colorvalid colored);
use Getopt::Long;
use File::Basename;
use JSON;

local $Term::ANSIColor::AUTORESET = 1;

our %program = (
  'NAME'      => 'FASTx N50 CALCULATOR',
  'AUTHOR'    => 'Andrea Telatin',
  'MAIL'      => 'andrea.telatin@quadram.ac.uk',
  'VERSION'   => '1.1',
);
my $opt_separator = "\t";
my $opt_format = 'default';
my %formats = (
  'default' => 'Prints only N50 for single file, TSV for multiple files',
  'tsv'     => 'Tab separated output (file, seqs, total size, N50)',
  'full'    => 'Not implemented',
  'json'    => 'JSON (JavaScript Object Notation) output',
  'short'   => 'Not Implemented',
  'csv'     => 'Alias for tsv',
  'custom'  => 'Custom format with --template STRING',
 );

my ($opt_help, 
	$opt_version, 
	$opt_input, 
	$opt_verbose, 
	$opt_debug, 
	$opt_color, 
	$opt_nonewline,
	$opt_noheader,
	$opt_pretty,
	$opt_basename,
	$opt_template,
);
our $tab  = "\t";
our $new  = "\n";
my $result = GetOptions(
    'f|format=s'    => \$opt_format,
    's|separator=s' => \$opt_separator,
    'p|pretty'      => \$opt_pretty,
    'n|nonewline'   => \$opt_nonewline,
    'j|noheader'    => \$opt_noheader,
    'b|basename'    => \$opt_basename,
    't|template=s'  => \$opt_template,
    'c|color'       => \$opt_color,
    'h|help'        => \$opt_help,
    'v|version'     => \$opt_version,
    'd|debug'       => \$opt_debug,
);

pod2usage({-exitval => 0, -verbose => 2}) if $opt_help;
version() if defined $opt_version;

our %output_object;

if (defined $opt_format) {
	$opt_format = lc($opt_format);
	if (!$formats{$opt_format}) {
		my @list = sort keys(%formats);

		die " FATAL ERROR:\n Output format not valid (--format '$opt_format').\n Use one of the following: " .
			join(', ',@list) . ".\n";
	}

	if ($formats{$opt_format} eq 'Not implemented') {
		print STDERR " WARNING: Format '$opt_format' not implemented yet. Switching to 'tsv'.\n";
		$opt_format = 'tsv';
	}

}
foreach my $file (@ARGV) {
	
	if (!-e "$file" and $file ne '-') {
		die " FATAL ERROR:\n File not found ($file).\n";	
	} elsif ($file eq '-') {
		$file = '<STDIN>';
	} else {
		open STDIN, '<', "$file" || die " FATAL ERROR:\n Unable to open file for reading ($file).\n";
	}



	my @aux;
	my %sizes;
	my ($n, $slen) = (0, 0);

	while (my ($name, $seq) = readfq(\*STDIN, \@aux)) {
	    ++$n;

	    my $size = length($seq);
	    $slen += $size;
	    $sizes{$size}++;
	}
	my $n50 = n50fromHash(\%sizes, $slen);

	say STDERR "[$file]\tTotalSize:$slen;N50:$n50;Sequences:$n" if ($opt_debug);
	
	$file = basename($file) if ($opt_basename);
	my %metrics = (
		'seqs' => $n,
		'N50'  => $n50,
		'size' => $slen,
	);
	$output_object{$file} = \%metrics;
}

my $file_num = scalar keys %output_object;

if (!$opt_format or $opt_format eq 'default') {
# DEFAULT
	if ($file_num == 1) {
		my @keys = keys %output_object;
		say $output_object{$keys[0]}{'N50'};
	} else {
		foreach my $r (keys %output_object) {
			say $r, $opt_separator ,$output_object{$r}{'N50'};
		}		
	}
} elsif ($opt_format eq 'json') {
	
	my $json = JSON->new->allow_nonref;
	my $pretty_printed = $json->pretty->encode( \%output_object );
	say $pretty_printed;

} elsif ($opt_format eq 'tsv' or $opt_format eq 'csv') {

	my @fields = ('path', 'seqs', 'size', 'N50');
	say '#', join($opt_separator, @fields) if (!defined $opt_noheader);

	foreach my $r (keys %output_object) {
		print $r,$opt_separator; 
		for (my $i = 1; $i <= $#fields; $i++) {
			print $output_object{$r}{$fields[$i]};
			if ($i == $#fields and !$opt_nonewline) {
				print "\n";
			} else {
				print $opt_separator;
			}

		}
	}
} elsif ($opt_format eq 'custom') {
	foreach my $r (keys %output_object) {
		my $output_string = $opt_template;
		$output_string =~s/{new}/$new/g;
		$output_string =~s/{tab}/$tab/g;
		$output_string =~s/{(\w+)}/$output_object{$r}{$1}/g;
		$output_string =~s/{path}/$r/g;
		print $output_string;
	}
}


sub debug {
	my ($message, $title) = @_;
	$title = 'INFO' unless defined $title;
	$title = uc($title);
	printMessage($message, $title, 'green', 'reset');
}
sub printMessage {
	my ($message, $title, $title_color, $message_color) = @_;
	$title_color   = 'reset' if (!defined $title_color or !colorvalid($title_color) or !$opt_color);
	$message_color = 'reset' if (!defined $message_color or !colorvalid($message_color) or !$opt_color);

	
	say STDERR colored("$title", $title_color), "\t", colored("$message", $message_color);
}
sub n50fromHash {
	my ($hash_ref, $total) = @_;
	my $tlen = 0;
	foreach my $s (sort {$a <=> $b} keys %{$hash_ref}) {
		$tlen += $s * ${$hash_ref}{$s};
		return $s if ($tlen >= ($total/2));
	}

}

sub version {
	printMessage("$program{NAME}, ver. $program{VERSION}", '', 'reset', 'bold green');
	printMessage(qq(
	$program{AUTHOR}

	Program to calculate N50 from multiple FASTA/FASTQ files.
	Type --help (or -h) to see the full documentation.), '', 'blue', 'green');
END

}
sub readfq {
    my ($fh, $aux) = @_;
    @$aux = [undef, 0] if (!(@$aux));
    return if ($aux->[1]);
    if (!defined($aux->[0])) {
        while (<$fh>) {
            chomp;
            if (substr($_, 0, 1) eq '>' || substr($_, 0, 1) eq '@') {
                $aux->[0] = $_;
                last;
            }
        }
        if (!defined($aux->[0])) {
            $aux->[1] = 1;
            return;
        }
    }

    my $name = '';
    if (defined $_) {
    	$name = /^.(\S+)/? $1 : '';
    }
    
    my $seq = '';
    my $c;
    $aux->[0] = undef;
    while (<$fh>) {
        chomp;
        $c = substr($_, 0, 1);
        last if ($c eq '>' || $c eq '@' || $c eq '+');
        $seq .= $_;
    }
    $aux->[0] = $_;
    $aux->[1] = 1 if (!defined($aux->[0]));
    return ($name, $seq) if ($c ne '+');
    my $qual = '';
    while (<$fh>) {
        chomp;
        $qual .= $_;
        if (length($qual) >= length($seq)) {
            $aux->[0] = undef;
            return ($name, $seq, $qual);
        }
    }
    $aux->[1] = 1;
    return ($name, $seq);
}

__END__

=head1 NAME
 
B<n50.pl> - A program to calculate N50 from FASTA/FASTQ files
 
=head1 AUTHOR
 
Andrea Telatin <andrea.telatin@quadram.ac.uk>

=head1 DESCRIPTION
 
This program parses a list of FASTA/FASTQ files calculating for each one
the number of sequences, the sum of sequences lengths and the N50.
It will print the result in different formats, by default only the N50 is
printed for a single file and all metrics in TSV format for multiple files.
 
=head1 SYNOPSIS
 
n50.pl [options] [FILE1 FILE2 FILE3...]

=head1 PARAMETERS

=over 12

=item I<-f, --format>

Output format: default, tsv, json, custom. 
See below for format specific switches.

=item I<-s, --separator>

Separator to be used in 'tsv' output. Default: tab.
The 'tsv' format will print a header line, followed
by a line for each file given as input with: file path,
as received, total number of sequences, total size in bp,
and finally N50.

=item I<-b, --basename>

Instead of printing the path of each file, will only print
the filename, stripping relative or absolute paths to it.

=item I<-j, --noheader>

When used with 'tsv' output format, will suppress header
line.

=item I<-n, --nonewline>

If used with 'default' or 'csv' output format, will NOT print the
newline character after the N50. Usually used in bash scripting.ù

=item I<-t, --template>

String to be used with 'custom' format. Will be used as template
string for each sample, replacing {new} with newlines, {tab} with
tab and {N50}, {seqs}, {size}, {path} with sample's N50, number of sequences,
total size in bp and file path respectively (the latter will
respect --basename if used).

=item I<-p, --pretty>

If used with 'json' output format, will format the JSON
in pretty print mode. Example:

 
 {
   "file1.fa" : {
     "size" : 290,
     "N50" : "290",
     "seqs" : 2
  },
   "file2.fa" : {
     "N50" : "456",
     "size" : 456,
     "seqs" : 2
  }
 }
 
=item I<-h, --help>

Will display this full help message and quit, even if other
arguments are supplied.

=back

=head1 COPYRIGHT
 
Copyright (C) 2017 Andrea Telatin 
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
=cut

