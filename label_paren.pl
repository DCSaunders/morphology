#!/usr/bin/perl
use strict;

while (<ARGV>)
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
