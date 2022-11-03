from hpccm.templates.git import git

Stage0 += baseimage(image='ubuntu:22.04', _distro="ubuntu22")
# Python (build-in python does not work with ubuntu 22)
Stage0 += apt_get(ospackages=['python2', 'python3'])

# Spack dependencies
ospackages = ['build-essential', 'make', 'patch', 'bash', 'tar', 'gzip', 'unzip', 'bzip2', 'xz-utils',
              'zstd', 'file', 'gnupg2', 'git', 'python3-dev', 'curl', 'ca-certificates', 'autoconf',
              'vim', 'pkg-config', 'gfortran']
Stage0 += apt_get(ospackages=ospackages)

# Setup and install Spack
spack_version = USERARG.get('spack_version', 'releases/v0.18')
Stage0 += shell(commands=[
    git().clone_step(repository='https://github.com/spack/spack', branch=spack_version, path='/opt'),
    'ln -s /opt/spack/share/spack/setup-env.sh /etc/profile.d/spack.sh',
    'ln -s /opt/spack/share/spack/spack-completion.bash /etc/profile.d'
])
Stage0 += environment(variables={'PATH': '/opt/spack/bin:/opt/view:$PATH', 'SPACK_ROOT': '/opt/spack'})

Stage0 += shell(commands=[
    'echo ". /opt/spack/share/spack/setup-env.sh" > /load-spack-env.sh',
    'echo "spack env activate /opt/spack-env" > /load-spack-env.sh'
])
