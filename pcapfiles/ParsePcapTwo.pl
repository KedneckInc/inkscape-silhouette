#!/usr/bin/env perl

use Data::Dumper;

my @tshark = qw( tshark -2 -V -x -r );

my $input = shift;
my $output = shift;

my @npclookup = qw( NUL SOH STX ETX EOT ENQ ACK BEL BS HT LF VT FF CR
                    SO SI DLE DC1 DC2 DC3 DC4 NAK SYN ETB CAN EM SUB
                    ESC FS GS RS US );

sub convert_raw(\@) {
        my $raw = shift;
        my @txt = ();
        my @result = ();
        for my $val ( @{$raw} ) {
                my $con = hex($val);
                if ( $con < 31 ) {
                        $con = $npclookup[$con];
                } elsif ( $con == 177 ) {
                        $con = "DEL";
                } elsif ( $con > 177 ) {
                        $con = "0x" . $val;
                } else {
                        $con = chr($con);
                }
                push( @txt, $con );
        }
        my $word = "";
        my $ignore_til_etx = 0;
        for my $val ( @txt ) {
                if ($ignore_til_etx) {
                        if ($val eq "ETX") {
                                $ignore_til_etx = 0;
                        }
                        next;
                }
                if ($val =~ m/^[\w\s,\.\!\[\\]$/) {
                        $word .= $val;
                        if ($word =~ m/^BE[12]/) {
                                push(@result,$word);
                                push(@result,"...");
                                push(@result,"ETX");
                                push(@result,"\n");
                                $ignore_til_etx = 1;
                        }
                } else {
                        if (length($word) > 0) {
                                push( @result, "'" . $word . "'" );
                                $word = "";
                        }
                        push( @result, $val );
                        if ( $val =~ m/^ETX$/ ) {
                                push( @result, "\n");
                        } elsif ( $val =~ m/^ENQ$/ ) {
                                if ( $result[ $#result - 2 ] =~ m/^ESC$/ ) {
                                        push(@result, "\n");
                                }
                        }
                }
        }
        return @result;
}

sub parse_excess_data(\@) {
        my $data = shift;
        my $rawdata = "";
        for my $line ( @{$data} ) {
                $line =~ s/^....\s+//; # Strip leading address.
                $line =~ s/^(([0-9a-f]{2,2} ){1,16})//;
                $rawdata .= $1;
        }
        my @alldata = split(" ",$rawdata);
        my @convdata = convert_raw(@alldata);
        pop(@convdata) if ($convdata[$#convdata] eq "\n");
        return split(" \n ",join(" ",@convdata));
}

open(INPUT, join(" ",@tshark,$input,"|") ) || die "Fatal: Cannot open tshark $input: $!\n";
open(OUTPUT, "> $output") || die "Fatal: Cannot open $output.\n";
my $oldframe = -1;
my @excessdata = ();
my $source;
my $destination;
my $newframe;
my @cmdresp;
while (<INPUT>) {
        if ( m/^Frame (\d+)/ ) {
                $newframe = $1;
                if ( $oldframe > -1 ) {
                        @cmdresp = parse_excess_data(@excessdata);
                        my $first = "";
                        if ( scalar(@cmdresp) > 0) {
                                $first = shift(@cmdresp);
                                print OUTPUT '"', join('","',$oldframe,$source,$destination,$first), qq("\n);
                                for my $data ( @cmdresp ) {
                                        print OUTPUT qq(,,,"), $data, qq("\n);
                                }
                        }
                }
                $oldframe = $newframe;
                @excessdata = ();
                @cmdresp = ();
                $source = $destination = "";
        } elsif ( m/^00[4-9a-f]0 / ) {
                chomp($_);
                push( @excessdata, $_ );
        } elsif ( m/\[Source: ([^\]]+)\]/ ) {
                $source = $1;
        } elsif ( m/\[Destination: ([^\]]+)\]/ ) {
                $destination = $1;
        }
}
close(OUTPUT);
close(INPUT);
