

#include <gromacs/fileio/xtcio.h>

int main(int argc, char *argv[])
{
	struct t_fileio * f = open_xtc("testfile.xtc", "w");//

    close_xtc(f);

    return 0;
}
