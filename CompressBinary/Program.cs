using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CompressBinary
{
    class Program
    {
        static void Main(string[] args)
        {
            using (var fs = new FileStream(@"D:\1.txt", FileMode.Open, FileAccess.Read))
            {
                var buffer = new byte[65535];
                var read = fs.Read(buffer, 0, buffer.Length);
                var realRead = new byte[read];
                Array.Copy(buffer, realRead, read);
                Compressor compressor = new Compressor();
                var compressed = compressor.SmallCompress(realRead);
                if (read != 0)
                {
                    Console.WriteLine("Compress: " + (compressed.Length * 100.0 / read) + "%");
                    Console.ReadKey();
                }
            }
        }
    }
}
