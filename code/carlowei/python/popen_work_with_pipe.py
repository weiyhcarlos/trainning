# -*- coding: UTF-8 -*- 
#!/bin/bash

import subprocess

#从管道读取数据
print '\nread:'
proc = subprocess.Popen(['echo', '"to stdout"'], 
                        stdout=subprocess.PIPE,
                        )
stdout_value = proc.communicate()[0]
print '\tstdout:', repr(stdout_value)


#从管道写入数据，给命令执行
print '\nwrite:'
proc = subprocess.Popen(['cat', '-'],
                        stdin=subprocess.PIPE,
                        )
proc.communicate('\tstdin: to stdin\n')


#从管道读写数据
print '\npopen3:'
proc = subprocess.Popen(['cat', '-'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
stdout_value = proc.communicate('through stdin to stdout')[0]
print '\tpass through:', repr(stdout_value)


#从管道读取stdout,stderr
print '\npopen3:'
proc = subprocess.Popen('cat -; echo "to stderr" 1>&2',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        )
stdout_value, stderr_value = proc.communicate('through stdin to stdout')
print '\tpass through:', repr(stdout_value)
print '\tstderr      :', repr(stderr_value)



#将错误输出到stdout,使用stderr=subprocess.STDOUT
print '\npopen4:'
proc = subprocess.Popen('cat -; echo "to stderr" 1>&2',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
stdout_value, stderr_value = proc.communicate('through stdin to stdout\n')
print '\tcombined output:', repr(stdout_value)
print '\tstderr value   :', repr(stderr_value)

#等同命令：cat popen_work_with_pipe.py | grep "popen" | cut -f 3 -d
print '\npopen5:'
cat = subprocess.Popen(['cat', 'popen_work_with_pipe.py'], 
                        stdout=subprocess.PIPE,
                        )

grep = subprocess.Popen(['grep', 'popen'],
                        stdin=cat.stdout,
                        stdout=subprocess.PIPE,
                        )

cut = subprocess.Popen(['cut', '-f', '3', '-d:'],
                        stdin=grep.stdout,
                        stdout=subprocess.PIPE,
                        )

end_of_pipe = cut.stdout

for line in end_of_pipe:
    print '\t', line.strip()
