#!/usr/bin/perl
use strict;

my $f_name = $ARGV[0];
open(my $in, "<", $f_name) 
    or die "$f_name not openable";

while (<$in>)
{
    chomp;
    my @toks = split(/ /);
    my @labels;
    foreach my $word (@toks){
	if (substr($word, 0, 1) eq '(') {
	    push @labels, substr($word, 1);
	}
	elsif (substr($word, 0, 1) eq ')'){
	    my $next_label = pop @labels;
	    print $next_label;
	}
	print "$word ";
    }
    print "\n"
}
