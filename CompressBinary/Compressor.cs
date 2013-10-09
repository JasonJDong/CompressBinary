using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CompressBinary
{
    public class Compressor
    {
        public byte[] SmallCompress(byte[] source)
        {
            var counter = new int[3];
            var compress = new List<byte>(13106);
            var left = new List<byte>(2048);
            for (int i = 0; i < source.Length - 1; i++)
            {
                var b = source[i];
                var next = source[i + 1];
                counter[1] = counter[2] == 0 ? i : counter[1];
                if (next == b)
                {
                    if (i < source.Length - 5 &&
                        counter[2] == 0 &&
                        b == source[i + 1] &&
                        b == source[i + 2] &&
                        b == source[i + 3] &&
                        b == source[i + 4] &&
                        b == source[i + 5])
                    {
                        counter[2] += 5;
                        i += 4;
                    }
                    else if (counter[2] > 0)
                    {
                        counter[2]++;
                    }
                    else
                    {
                        left.Add(b);
                        continue;
                    }
                    counter[0] = b;
                }
                else
                {
                    if (counter[2] > 0)
                    {
                        compress.Add(BitConverter.GetBytes(counter[0])[0]);
                        var c1 = BitConverter.GetBytes(counter[1]);
                        var c2 = BitConverter.GetBytes(counter[2]);
                        compress.Add(c1[0]);
                        compress.Add(c1[1]);
                        compress.Add(c2[0]);
                        compress.Add(c2[1]);
                        counter = new int[3];
                    }
                    else
                    {
                        left.Add(b);
                    }
                }
            }
            if (compress.Count == 0)
            {
                return source;
            }
            var temp = new List<byte>(compress.Count + left.Count + 2);
            temp.AddRange(BitConverter.GetBytes(compress.Count));
            temp.AddRange(compress);
            temp.AddRange(left);
            return temp.ToArray();
        }

        public byte[] SmallDecompress(byte[] source)
        {
            var lengthBytes = new byte[4];
            Array.Copy(source, lengthBytes, 4);
            var length = BitConverter.ToInt32(lengthBytes, 0);
            var compress = new byte[length];
            Array.Copy(source, 4, compress, 0, compress.Length);
            var left = new byte[source.Length - length - 4];
            Array.Copy(source, length + 4, left, 0, left.Length);
            var decompress = new LinkedList<byte>();
            var posDecompress = new LinkedListNode<byte>[left.Length];
            for (int i = 0; i < left.Length; i++)
            {
                posDecompress[i] = decompress.AddLast(left[i]);

            }
            for (int i = 0; i < compress.Length; i += 5)
            {
                var value = compress[i];
                var posBytes = new byte[4];
                posBytes[0] = compress[i + 1];
                posBytes[1] = compress[i + 2];
                posBytes[2] = posBytes[3] = 0;
                var position = BitConverter.ToInt32(posBytes, 0);
                var lenBytes = new byte[4];
                lenBytes[0] = compress[i + 3];
                lenBytes[1] = compress[i + 4];
                lenBytes[2] = lenBytes[3] = 0;
                var len = BitConverter.ToInt32(lenBytes, 0);
                if (position >= decompress.Count)
                {
                    for (int j = 0; j < len; j++)
                    {
                        decompress.AddLast(value);
                    }
                }
                else
                {
                    var node = posDecompress[position];
                    for (int j = 0; j < len; j++)
                    {
                        decompress.AddBefore(node, value);
                    }
                }
            }
            return decompress.ToArray();
        }
    }
}
