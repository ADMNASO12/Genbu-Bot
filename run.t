#!/usr/bin/perl
sub check_tools {
    my ($cmd) = @_;
    my $found = system("which $cmd > /dev/null 2>&1") == 0; # Linux only.
}

sub gen_venv {
    my $venv = ".venv";

    if (! -d $venv) {
        print "Could not find $venv. Generate now\n";
        system("python -m venv .venv");
    }
}

sub run_test {
    my $test = "main_t.py";
    if (! -e $test ) {
        die "Could not find test file. Stop now.\n";
    }

    system("python main_t.py")
}

my $python = "python";
check_tools(python);
gen_venv();
run_test()