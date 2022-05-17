if [ $1 == 1 ]
then
    python -m scr.print
    #python -m scr.get_images
elif [ $1 == 2 ]
then
    python -m scr.get_data
else
    echo "enter either pic or data"
fi
#python -m scr.attem
#python -m scr.main