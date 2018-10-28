#!/usr/bin/env perl

my $source;
my $destination;
my $type;
my $request;
my $port;
my $data;
my $frame;
my $resin;
my $reqin;

print "FRAME,REQ,RESP,SRC,DEST,TYPE,REQUEST,PORT,'DATA'\n";

while(<STDIN>) {

        s/[\r\n]+$//;

        if ( m/^Frame (\d+):/ ) {

                $frame = $1;
                $source = $destination = $type = $request = "";
                $resin = $reqin = $data = $port = "";
                next;
        }

        next if m/^\s+(Encapsulation|Arrival|.Time|Frame|.Frame|.Protocols|Capture Length)/;
        next if m/^\s+(Epoch|URB id|Device|URB bus|Data|URB u?sec|URB status)/;
        next if m/^\s+(URB transfer|Endpoint|=|URB length|Response in|Interval|Start frame|Copy of Transfer|Number of ISO)/;
        next if m/^(wValue|wIndex|wLength|\s+.zero.|USB URB)/;
        next if m/\[bInterfaceClass:/;
        next if m/Direction: (IN|OUT)/;
        next if m/Endpoint number:/;
        next if m/Unused Setup Header/;
        next if m/: (False|Default colors)/;
        next if m/(bmRequestType:|= Direction:|= Type:|= Recipient:|Descriptor Index:|bDescriptorType:|Language Id:|wLength:|PortFeatureSelector:|PortSelector:)/;
        next if m/^URB setup/;
        next if m/= PORT_/;
        next if m/= C_PORT_/;
        next if m/^\s+Interface id:/;
        next if m/^\s+Interface name:/;

        if ( m/\[Source: (.+)\]/ ) {$source = $1; next;}
        if ( m/\[Destination: (.+)\]/ ) {$destination = $1; next;}
        if ( m/URB type: (.*)$/ ) {$type = $1; next;}
        if ( m/bRequest: (.*)$/ ) {$request = $1; next;}
        if ( m/^\s+Port: (\d+)/ ) {$port = $1; next;}
        if ( m/Leftover Capture Data: (.*)/ ) {
                $data = $1; next;
        }
        if ( m/\[Response in: (\d+)/ ) {
                $resin = $1;
                next;
        }
        if ( m/\[Request in: (\d+)/ ) {
                $reqin = $1;
                next;
        }

        if ( m/^0000  / ) {
                print qq($frame,$reqin,$resin,$source,$destination,$type,$request,$port,"$data"\n);
                next;
        }

        next if ( m/^00[123]0  / );

        next if ( m/^\s+0040  1b 05\s*$/ );
        next if ( m/^\s+0040  3[0-9] 03\s*$/ );

        next if m/^\s*$/;

        print ',,,,,,,,"';
        print $_;
        print '"', "\n";
}
