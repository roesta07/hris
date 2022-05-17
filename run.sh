if [ $1 == "data" ]
then
    python -m scr.print
    #python -m scr.get_images
elif [ $1 == "image" ]
then
    python -m scr.get_data
else
    echo "enter either pic or data"
fi