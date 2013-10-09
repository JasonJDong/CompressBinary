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
            var file = Path.Combine(Environment.CurrentDirectory, "1.txt");
            using (var fs = new FileStream(file, FileMode.Open, FileAccess.Read))
            {
                var buffer = new byte[65535];
                var read = fs.Read(buffer, 0, buffer.Length);
                var realRead = new byte[read];
                Array.Copy(buffer, realRead, read);
                Compressor compressor = new Compressor();
                var compressed = compressor.SmallCompress(realRead);
                var decompress = compressor.SmallDecompress(compressed);
                if (read != 0)
                {
                    Console.WriteLine("Compress: " + (compressed.Length * 100.0 / read) + "%");
                    Console.ReadKey();
                }
            }
        }
    }
}
