from filesystem import Session

class Session(Session):
  def __init__(self, fs):
    super().__init__(fs)

  # you can add any helper function here, if needed

  # This removes the directory dir_name from the current working directory
  # It should report errors when
  #   * dir_name does not exist
  #   * dir_name is not empty
  #   * dir_name is not a directory
  def rmdir(self, dir_name):
    target_node = None
    for child in self.curr_dir.children:
      if child.name == dir_name:
        target_node = child
        break

    # The directory does not exist
    if target_node is None:
      print(f'{dir_name} does not exist!')
      return

    # The target is not a directory
    if target_node.node_type != 'directory':
      print(f'{dir_name} is not a directory!')
      return

    # The directory is not empty
    if len(target_node.children) > 0:
      print(f'{dir_name} is not empty!')
      return
    
    # remove the node from the parent's list of children
    self.curr_dir.children.remove(target_node)

  # this removes a file "file_name" from the current working directory
  # it should report errors when:
  #   * file_name does not exist
  #   * file_name is a irectory
  def rm(self, file_name):
    target_node = None
    for child in self.curr_dir.children:
      if child.name == file_name:
        target_node = child
        break
    
    # The file does not exist
    if target_node is None:
      print(f'{file_name} does not exist!')
      return
    
    # The target is a directory
    if target_node.node_type == 'directory':
      print(f'{file_name} is a directory!')
      return
    
    # Remove the file
    self.curr_dir.children.remove(target_node)

    
  # This emulates the hdfs oiv (offline image viewer) command to print the
  # entire namespace of file system. In other words, it lists all file system
  # objects (file or directory), one line at a time. For each object,
  # it shows the path to the object and the type of object, seperated by comma.
  # For example,
  #           /,directory
  #           /home,directory
  #           /home/john,directory
  #           /home/john/hw1.py,file
  #           ...
  #
  def dump_fsimage(self):
    # a nested function to traverse the file system tree
    def _traverse(node, path):
      print(f'{path},{node.node_type}')
      # recursively traverse the children if node is a directory
      for child in node.children:
        if path == '/':
          # if parent is root then path should be /child_name
          child_path = f'/{child.name}'
        else:
          child_path = f'{path}/{child.name}'
        
        _traverse(child, child_path)
    
    # start traversing from the root
    if self.root:
      _traverse(self.root, '/')
