 while (1)
    {
        if (currnum > 9){ //Two digit print
            tens = getArray(currnum / 10);
            ones = getArray(currnum % 10);
            for (int i = 0;i<64;++i) //Rows
            {
                if (i == 12)
                {
                    print = 1;
                }
                if (i == 52)
                {
                    print = 0;
                }
                for (int j = 0;j<128;++j) // Col addresses
                {
                    if ( print && j > 47 && j < 61)
                    {
                        Snd_Disp_word(tens[i-12][j-48],1);
                    }
                    else if ( print && j > 66 && j < 80)
                    {
                        Snd_Disp_word(ones[i-12][j-67],1);
                    }
                    else
                    {Snd_Disp_word(0x00,1);}
                };
            };

        }
        else
        {
            ones = getArray(currnum);
        //One digit print
            for (int i = 0;i<64;++i) //Rows
            {
                for (int j = 0;j<128;++j) // Col addresses
                {
                    if ( i > 11 && i < 52 && j > 57 && j < 71)
                    {
                        Snd_Disp_word(ones[i-12][j-58],1);
                    }
                    else
                    {
                        Snd_Disp_word(0x00,1);
                    }
                };
            };
        }
        
        //DelayForNms(1);
        ++currnum;
        if (currnum == 88)
        {
            currnum = 0;
        }
