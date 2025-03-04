.. _getting-started:

Getting Started
===============

This tutorial walks you through a simple example of using LeanDojo to extract data and interact with Lean. 
LeanDojo supports both Lean 3 and Lean 4.


Requirements
************

* Supported platforms: Linux, Windows (WSL), and macOS (experimental for Apple silicon)
* Git >= 2.25
* 3.9 <= Python < 3.11
* wget
* `elan <https://github.com/leanprover/elan>`_
* `Docker <https://www.docker.com/>`_ strongly recommended when using LeanDojo with Lean 3. See :ref:`running-within-docker` if it is not an option for you
* Recommended: Generate a `GitHub personal access token <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#personal-access-tokens-classic>`_ and set the environment variable :code:`GITHUB_ACCESS_TOKEN` to it

Installation
************

LeanDojo is available on `PyPI <https://pypi.org/project/lean-dojo/>`_ and can be installed via :code:`pip install lean-dojo`.
Alternatively, you can install the most recent version by running :code:`pip install .` locally in the root directory of `LeanDojo's GitHub repo <https://github.com/lean-dojo/LeanDojo>`_.


.. _extracting-data-from-lean3:

Extracting Data from Lean 3
***************************
LeanDojo enables extracting data from any repo in any recent version of Lean 3 (at least :code:`v3.42.1`). 
We use `lean-example <https://github.com/yangky11/lean-example>`_ as a simple example,
which has a single Lean file with the theorem:

.. code-block:: lean
   :caption: example.lean

   open nat (add_assoc add_comm)

   theorem hello_world (a b c : ℕ) : a + b + c = a + c + b :=
   begin
     rw [add_assoc, add_comm b, ←add_assoc]
   end

When using LeanDojo with Lean 3, you are strongly encouraged to have Docker installed and 
set the environment variable :code:`CONTAINER` to :code:`docker`. Now we launch a Python 
REPL session by :code:`CONTAINER=docker ipython` and use LeanDojo to trace the repo in Python by specifying its URL and a commit hash:

.. code-block:: python

   import os
   from lean_dojo import LeanGitRepo, trace

   assert os.environ["CONTAINER"] == "docker"
   repo = LeanGitRepo("https://github.com/yangky11/lean-example", "5a0360e49946815cb53132638ccdd46fb1859e2a")
   trace(repo, dst_dir="traced_lean-example")

After ~10 minutes (depending on how many CPUs you have), it generates a :file:`traced_lean-example` directory with the subdirectories below.
Please check out :ref:`troubleshooting` if you encounter any issue.

::

   traced_lean-example
   └─lean-example
     ├─_target
     │ └─deps
     │   └─lean
     └─...

:file:`lean` is the traced `Lean repo <https://github.com/leanprover-community/lean>`_, 
and :file:`lean-example` is the traced example repo. We call them "traced" because each
:file:`*.lean` file is accompanied by the following files:
 
* :file:`*.olean`: Lean's compiled object file. 
* :file:`*.dep_paths`: Paths of dependencies imported by the current file. 
* :file:`*.ast.json`: ASTs exported by :code:`lean --ast --tsast --tspp` 
* :file:`*.trace.xml`: Syntactic and semantic information extracted from Lean.  

The most important one is :file:`*.trace.xml`. For example, below is :file:`traced_lean-example/lean-example/src/example.trace.xml`:

.. code-block::
   :caption: example.trace.xml

   <TracedFile path="src/example.lean" md5="c0cebeb0e7374edc9405ef40dc5689d8">
     <FileNode start="(0, 1)" end="(5, 4)" id="1">
       <ImportsNode start="(1, 1)" end="(1, 1)" id="2"/>
       <CommandsNode start="(1, 1)" end="(1, 1)" id="3">
         <OpenNode start="(1, 1)" end="(1, 30)" id="4" namespaces="[]">
           <GroupNode start="(1, 6)" end="(1, 6)" id="5">
             <IdentNode start="(1, 6)" end="(1, 6)" id="6" ident="nat"/>
             <ExplicitNode start="(1, 10)" end="(1, 11)" id="7">
               <IdentNode start="(1, 11)" end="(1, 11)" id="8" ident="add_assoc"/>
               <IdentNode start="(1, 21)" end="(1, 21)" id="9" ident="add_comm"/>
             </ExplicitNode>
           </GroupNode>
         </OpenNode>
         <TheoremNode start="(3, 1)" end="(6, 4)" id="10" name="hello_world" full_name="hello_world">
           <IdentNode start="(3, 9)" end="(3, 9)" id="11" ident="hello_world"/>
           <BindersNode start="(3, 21)" end="(3, 21)" id="12">
             <OtherNode start="(3, 22)" end="(3, 22)" id="14" kind="binder_0">
               <VarsNode start="(3, 22)" end="(3, 22)" id="13">
                 <IdentNode start="(3, 22)" end="(3, 22)" id="15" ident="a"/>
                 <IdentNode start="(3, 24)" end="(3, 24)" id="16" ident="b"/>
                 <IdentNode start="(3, 26)" end="(3, 26)" id="17" ident="c"/>
               </VarsNode>
               <NotationNode start="(3, 30)" end="(3, 31)" id="18" value="exprℕ"/>
             </OtherNode>
           </BindersNode>
           <NotationNode start="(3, 45)" end="(3, 56)" id="29" value="expr = ">
             <NotationNode start="(3, 41)" end="(3, 44)" id="23" value="expr + ">
               <NotationNode start="(3, 37)" end="(3, 40)" id="21" value="expr + ">
                 <IdentNode start="(3, 35)" end="(3, 36)" id="19" ident="a"/>
                 <IdentNode start="(3, 39)" end="(3, 40)" id="20" ident="b"/>
               </NotationNode>
               <IdentNode start="(3, 43)" end="(3, 44)" id="22" ident="c"/>
             </NotationNode>
             <NotationNode start="(3, 53)" end="(3, 56)" id="28" value="expr + ">
               <NotationNode start="(3, 49)" end="(3, 52)" id="26" value="expr + ">
                 <IdentNode start="(3, 47)" end="(3, 48)" id="24" ident="a"/>
                 <IdentNode start="(3, 51)" end="(3, 52)" id="25" ident="c"/>
               </NotationNode>
               <IdentNode start="(3, 55)" end="(3, 56)" id="27" ident="b"/>
             </NotationNode>
           </NotationNode>
           <NotationNode start="(4, 1)" end="(6, 4)" id="47" value="begin">
             <BeginNode start="(4, 1)" end="(6, 4)" id="30">
               <TacticNode start="(5, 3)" end="(5, 41)" id="31" tactic="rw [add_assoc, add_comm b, ←add_assoc]" state_before="a b c : ℕ&#10;⊢ a + b + c = a + c + b" state_after="no goals">
                 <ParseNode start="(5, 6)" end="(5, 41)" id="32">
                   <TokenNode start="(5, 6)" end="(5, 6)" id="33" token="["/>
                   <ExprNode start="(5, 7)" end="(5, 16)" id="35">
                     <IdentNode start="(5, 7)" end="(5, 16)" id="34" ident="add_assoc" expr="2" full_name="nat.add_assoc" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(22, 17)"/>
                   </ExprNode>
                   <TokenNode start="(5, 16)" end="(5, 16)" id="36" token=","/>
                   <ExprNode start="(5, 18)" end="(5, 28)" id="40">
                     <AppNode start="(5, 18)" end="(5, 28)" id="39">
                       <IdentNode start="(5, 18)" end="(5, 26)" id="37" ident="add_comm" expr="1" full_name="nat.add_comm" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(15, 17)"/>
                       <IdentNode start="(5, 27)" end="(5, 28)" id="38" ident="b"/>
                     </AppNode>
                   </ExprNode>
                   <TokenNode start="(5, 28)" end="(5, 28)" id="41" token=","/>
                   <TokenNode start="(5, 30)" end="(5, 30)" id="42" token="&amp;lt;-"/>
                   <ExprNode start="(5, 31)" end="(5, 40)" id="44">
                     <IdentNode start="(5, 31)" end="(5, 40)" id="43" ident="add_assoc" expr="0" full_name="nat.add_assoc" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(22, 17)"/>
                   </ExprNode>
                   <TokenNode start="(5, 40)" end="(5, 40)" id="45" token="]"/>
                 </ParseNode>
                 <ParseNode start="(6, 1)" end="(5, 41)" id="46"/>
               </TacticNode>
             </BeginNode>
           </NotationNode>
         </TheoremNode>
       </CommandsNode>
     </FileNode>
     <Exprs>
       <ConstExpr tags="0" full_name="nat.add_assoc" levels="[]" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(22, 17)"/>
       <ConstExpr tags="1" full_name="nat.add_comm" levels="[]" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(15, 17)"/>
       <ConstExpr tags="2" full_name="nat.add_assoc" levels="[]" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(22, 17)"/>
     </Exprs>
     <Comments/>
   </TracedFile>


It contains a lot of information not readily available in the original :file:`*.lean` files. 
For example, by looking at 

.. code-block::

   <IdentNode start="(5, 7)" end="(5, 16)" id="34" ident="add_assoc" expr="2" full_name="nat.add_assoc" def_path="_target/deps/lean/library/init/data/nat/lemmas.lean" def_pos="(22, 17)"/>

, we know that the :code:`add_assoc` used in line 5 column 7–16 of :file:`example.lean` 
has the full name :code:`nat.add_assoc` and is defined at line 22 column 17 of :file:`lean/library/init/data/nat/lemmas.lean`. 
This kind of information is critical downstream tasks, e.g., developing learning-based theorem provers that can perform premise selection.


Interacting with Lean 3
***********************

LeanDojo can also be used for programmatic interaction with Lean. Below we prove the :code:`hello_world` 
theorem in the previous example. The `lean-example <https://github.com/yangky11/lean-example>`_ repo
has to be traced before interacting with any theorem in it. So the code below will first take some time 
to trace the repo if you haven't followed the steps in :ref:`extracting-data-from-lean3`. The tracing has to be done 
only once, and the traced repo will be cached for future use. Some repos do not need to be traced locally and 
can be downloaded from `our AWS S3 <https://lean-dojo.s3.amazonaws.com>`_ (see :ref:`caching` for details).

.. code-block:: python

   import os
   from lean_dojo import *

   assert os.environ["CONTAINER"] == "docker"
   repo = LeanGitRepo("https://github.com/yangky11/lean-example", "5a0360e49946815cb53132638ccdd46fb1859e2a")
   theorem = Theorem(repo, "src/example.lean", "hello_world")

   with Dojo(theorem) as (dojo, init_state):
     print(init_state)
     result = dojo.run_tac(init_state, "rw [add_assoc, add_comm b, ←add_assoc]")
     assert isinstance(result, ProofFinished)
     print(result)

.. code-block::
   :caption: Expected output:

   TacticState(pp='a b c : ℕ\n⊢ a + b + c = a + c + b', id=0, message=None)
   ProofFinished(tactic_state_id=1, message='')


.. _extracting-data-from-lean4:

Extracting Data from Lean 4
***************************
LeanDojo can also extract data from Lean 4 repos. We use `lean4-example <https://github.com/yangky11/lean4-example>`_ as a simple example,
which has a single Lean file with the theorem:

.. code-block:: lean
   :caption: Lean4Example.lean

    open Nat (add_assoc add_comm)

    def hello := "world"

    theorem hello_world (a b c : Nat) 
      : a + b + c = a + c + b := by 
      rw [add_assoc, add_comm b, ←add_assoc]

We use LeanDojo to trace the repo in Python by specifying its URL and a commit hash:

.. code-block:: python

   from lean_dojo import LeanGitRepo, trace

   repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "fd14c4c8b29cc74a082e5ae6f64c2fb25b28e15e")
   trace(repo, dst_dir="traced_lean4-example")

After a few minutes or one hour (depending on #CPUs), it generates a :file:`traced_lean4-example` directory with the subdirectories below.
The directory structure is different from that of Lean 3, as Lean 4 uses a different build system. 
Please check out :ref:`troubleshooting` if you encounter any issue.

::

   traced_lean4-example
   └─lean4-example
     ├─.lake
     │ ├─packages
     │ │ └─lean4
     │ └─build
     │   ├─ir
     │   │ ├─Lean4Example.dep_paths
     │   │ ├─Lean4Example.ast.json
     │   │ └─Lean4Example.trace.xml
     │   └─lib
     │     └─Lean4Example.olean
     ├─Lean4Example.lean
     └─...

:file:`lean4` is the traced `Lean 4 repo <https://github.com/leanprover/lean4>`_, 
and :file:`lean-example` is the traced example repo. We call them "traced" because each
:file:`*.lean` file is accompanied by the following files:
 
* :file:`*.olean`: Lean's compiled object file. 
* :file:`*.dep_paths`: Paths of dependencies imported by the current file. 
* :file:`*.ast.json`: ASTs exported by `ExtractData.lean <https://github.com/lean-dojo/LeanDojo/blob/main/src/lean_dojo/data_extraction/ExtractData.lean>`_.
* :file:`*.trace.xml`: Syntactic and semantic information extracted from Lean.  

The most important one is :file:`*.trace.xml`. Its format is different from Lean 3. 
For example, below is :file:`traced_lean4-example/lean4-example/.lake/build/ir/Lean4Example.trace.xml`:

.. code-block::
   :caption: Lean4Example.trace.xml

   <TracedFile path="Lean4Example.lean" md5="f8eb6563cd78c62389ff6cf40f485a1e">
     <FileNode4 start="(1, 1)" end="(7, 53)">
       <ModuleHeaderNode4>
         <NullNode4/>
         <NullNode4/>
       </ModuleHeaderNode4>
       <CommandOpenNode4 start="(1, 1)" end="(1, 30)">
         <AtomNode4 start="(1, 1)" end="(1, 5)" leading="" trailing=" " val="open"/>
         <CommandOpenonlyNode4 start="(1, 6)" end="(1, 30)">
           <IdentNode4 start="(1, 6)" end="(1, 9)" leading="" trailing=" " raw_val="Nat" val="Nat"/>
           <AtomNode4 start="(1, 10)" end="(1, 11)" leading="" trailing="" val="("/>
           <NullNode4 start="(1, 11)" end="(1, 29)">
             <IdentNode4 start="(1, 11)" end="(1, 20)" leading="" trailing=" " raw_val="add_assoc" val="add_assoc" full_name="Nat.add_assoc" mod_name="Init.Data.Nat.Basic" def_path=".lake/packages/lean4/src/lean/Init/Data/Nat/Basic.lean" def_start="(138, 19)" def_end="(138, 28)"/>
             <IdentNode4 start="(1, 21)" end="(1, 29)" leading="" trailing="" raw_val="add_comm" val="add_comm" full_name="Nat.add_comm" mod_name="Init.Data.Nat.Basic" def_path=".lake/packages/lean4/src/lean/Init/Data/Nat/Basic.lean" def_start="(131, 19)" def_end="(131, 27)"/>
           </NullNode4>
           <AtomNode4 start="(1, 29)" end="(1, 30)" leading="" trailing="&#10;&#10;" val=")"/>
         </CommandOpenonlyNode4>
       </CommandOpenNode4>
       <CommandDeclarationNode4 start="(3, 1)" end="(5, 41)" name="hello_world" full_name="hello_world">
         <CommandDeclmodifiersNode4>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
         </CommandDeclmodifiersNode4>
         <CommandTheoremNode4 start="(3, 1)" end="(5, 41)" name="hello_world" full_name="hello_world" _is_private_decl="False">
           <AtomNode4 start="(3, 1)" end="(3, 8)" leading="" trailing=" " val="theorem"/>
           <CommandDeclidNode4 start="(3, 9)" end="(3, 20)">
             <IdentNode4 start="(3, 9)" end="(3, 20)" leading="" trailing=" " raw_val="hello_world" val="hello_world"/>
             <NullNode4/>
           </CommandDeclidNode4>
           <CommandDeclsigNode4 start="(3, 21)" end="(4, 26)">
             <NullNode4 start="(3, 21)" end="(3, 34)">
               <TermExplicitbinderNode4 start="(3, 21)" end="(3, 34)">
                 <AtomNode4 start="(3, 21)" end="(3, 22)" leading="" trailing="" val="("/>
                 <NullNode4 start="(3, 22)" end="(3, 27)">
                   <IdentNode4 start="(3, 22)" end="(3, 23)" leading="" trailing=" " raw_val="a" val="a"/>
                   <IdentNode4 start="(3, 24)" end="(3, 25)" leading="" trailing=" " raw_val="b" val="b"/>
                   <IdentNode4 start="(3, 26)" end="(3, 27)" leading="" trailing=" " raw_val="c" val="c"/>
                 </NullNode4>
                 <NullNode4 start="(3, 28)" end="(3, 33)">
                   <AtomNode4 start="(3, 28)" end="(3, 29)" leading="" trailing=" " val=":"/>
                   <IdentNode4 start="(3, 30)" end="(3, 33)" leading="" trailing="" raw_val="Nat" val="Nat" full_name="Nat" mod_name="Init.Prelude" def_path=".lake/packages/lean4/src/lean/Init/Prelude.lean" def_start="(1044, 11)" def_end="(1044, 14)"/>
                 </NullNode4>
                 <NullNode4/>
                 <AtomNode4 start="(3, 33)" end="(3, 34)" leading="" trailing="&#10;  " val=")"/>
               </TermExplicitbinderNode4>
             </NullNode4>
             <TermTypespecNode4 start="(4, 3)" end="(4, 26)">
               <AtomNode4 start="(4, 3)" end="(4, 4)" leading="" trailing=" " val=":"/>
               <OtherNode4 start="(4, 5)" end="(4, 26)" kind="«term_=_»">
                 <OtherNode4 start="(4, 5)" end="(4, 14)" kind="«term_+_»">
                   <OtherNode4 start="(4, 5)" end="(4, 10)" kind="«term_+_»">
                     <IdentNode4 start="(4, 5)" end="(4, 6)" leading="" trailing=" " raw_val="a" val="a"/>
                     <AtomNode4 start="(4, 7)" end="(4, 8)" leading="" trailing=" " val="+"/>
                     <IdentNode4 start="(4, 9)" end="(4, 10)" leading="" trailing=" " raw_val="b" val="b"/>
                   </OtherNode4>
                   <AtomNode4 start="(4, 11)" end="(4, 12)" leading="" trailing=" " val="+"/>
                   <IdentNode4 start="(4, 13)" end="(4, 14)" leading="" trailing=" " raw_val="c" val="c"/>
                 </OtherNode4>
                 <AtomNode4 start="(4, 15)" end="(4, 16)" leading="" trailing=" " val="="/>
                 <OtherNode4 start="(4, 17)" end="(4, 26)" kind="«term_+_»">
                   <OtherNode4 start="(4, 17)" end="(4, 22)" kind="«term_+_»">
                     <IdentNode4 start="(4, 17)" end="(4, 18)" leading="" trailing=" " raw_val="a" val="a"/>
                     <AtomNode4 start="(4, 19)" end="(4, 20)" leading="" trailing=" " val="+"/>
                     <IdentNode4 start="(4, 21)" end="(4, 22)" leading="" trailing=" " raw_val="c" val="c"/>
                   </OtherNode4>
                   <AtomNode4 start="(4, 23)" end="(4, 24)" leading="" trailing=" " val="+"/>
                   <IdentNode4 start="(4, 25)" end="(4, 26)" leading="" trailing=" " raw_val="b" val="b"/>
                 </OtherNode4>
               </OtherNode4>
             </TermTypespecNode4>
           </CommandDeclsigNode4>
           <CommandDeclvalsimpleNode4 start="(4, 27)" end="(5, 41)">
             <AtomNode4 start="(4, 27)" end="(4, 29)" leading="" trailing=" " val=":="/>
             <TermBytacticNode4 start="(4, 30)" end="(5, 41)">
               <AtomNode4 start="(4, 30)" end="(4, 32)" leading="" trailing="&#10;  " val="by"/>
               <TacticTacticseqNode4 start="(5, 3)" end="(5, 41)">
                 <TacticTacticseq1IndentedNode4 start="(5, 3)" end="(5, 41)">
                   <NullNode4 start="(5, 3)" end="(5, 41)">
                     <OtherNode4 start="(5, 3)" end="(5, 41)" kind="Lean.Parser.Tactic.rwSeq" state_before="a b c : Nat&#10;⊢ a + b + c = a + c + b" state_after="no goals" tactic="rw [add_assoc, add_comm b, ←add_assoc]">
                       <AtomNode4 start="(5, 3)" end="(5, 5)" leading="" trailing=" " val="rw"/>
                       <NullNode4/>
                       <OtherNode4 start="(5, 6)" end="(5, 41)" kind="Lean.Parser.Tactic.rwRuleSeq">
                         <AtomNode4 start="(5, 6)" end="(5, 7)" leading="" trailing="" val="["/>
                         <NullNode4 start="(5, 7)" end="(5, 40)">
                           <OtherNode4 start="(5, 7)" end="(5, 16)" kind="Lean.Parser.Tactic.rwRule">
                             <NullNode4/>
                             <IdentNode4 start="(5, 7)" end="(5, 16)" leading="" trailing="" raw_val="add_assoc" val="add_assoc" full_name="Nat.add_assoc" mod_name="Init.Data.Nat.Basic" def_path=".lake/packages/lean4/src/lean/Init/Data/Nat/Basic.lean" def_start="(138, 19)" def_end="(138, 28)"/>
                           </OtherNode4>
                           <AtomNode4 start="(5, 16)" end="(5, 17)" leading="" trailing=" " val=","/>
                           <OtherNode4 start="(5, 18)" end="(5, 28)" kind="Lean.Parser.Tactic.rwRule">
                             <NullNode4/>
                             <OtherNode4 start="(5, 18)" end="(5, 28)" kind="Lean.Parser.Term.app">
                               <IdentNode4 start="(5, 18)" end="(5, 26)" leading="" trailing=" " raw_val="add_comm" val="add_comm" full_name="Nat.add_comm" mod_name="Init.Data.Nat.Basic" def_path=".lake/packages/lean4/src/lean/Init/Data/Nat/Basic.lean" def_start="(131, 19)" def_end="(131, 27)"/>
                               <NullNode4 start="(5, 27)" end="(5, 28)">
                                 <IdentNode4 start="(5, 27)" end="(5, 28)" leading="" trailing="" raw_val="b" val="b"/>
                               </NullNode4>
                             </OtherNode4>
                           </OtherNode4>
                           <AtomNode4 start="(5, 28)" end="(5, 29)" leading="" trailing=" " val=","/>
                           <OtherNode4 start="(5, 30)" end="(5, 40)" kind="Lean.Parser.Tactic.rwRule">
                             <NullNode4 start="(5, 30)" end="(5, 31)">
                               <OtherNode4 start="(5, 30)" end="(5, 31)" kind="patternIgnore">
                                 <OtherNode4 start="(5, 30)" end="(5, 31)" kind="token.«← »">
                                   <AtomNode4 start="(5, 30)" end="(5, 31)" leading="" trailing="" val="←"/>
                                 </OtherNode4>
                               </OtherNode4>
                             </NullNode4>
                             <IdentNode4 start="(5, 31)" end="(5, 40)" leading="" trailing="" raw_val="add_assoc" val="add_assoc" full_name="Nat.add_assoc" mod_name="Init.Data.Nat.Basic" def_path=".lake/packages/lean4/src/lean/Init/Data/Nat/Basic.lean" def_start="(138, 19)" def_end="(138, 28)"/>
                           </OtherNode4>
                         </NullNode4>
                         <AtomNode4 start="(5, 40)" end="(5, 41)" leading="" trailing="&#10;&#10;" val="]"/>
                       </OtherNode4>
                       <NullNode4/>
                     </OtherNode4>
                   </NullNode4>
                 </TacticTacticseq1IndentedNode4>
               </TacticTacticseqNode4>
             </TermBytacticNode4>
             <NullNode4/>
           </CommandDeclvalsimpleNode4>
           <NullNode4/>
           <NullNode4/>
         </CommandTheoremNode4>
       </CommandDeclarationNode4>
       <CommandDeclarationNode4 start="(7, 1)" end="(7, 53)" name="foo" full_name="foo">
         <CommandDeclmodifiersNode4>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
           <NullNode4/>
         </CommandDeclmodifiersNode4>
         <CommandTheoremNode4 start="(7, 1)" end="(7, 53)" name="foo" full_name="foo" _is_private_decl="False">
           <AtomNode4 start="(7, 1)" end="(7, 8)" leading="" trailing=" " val="theorem"/>
           <CommandDeclidNode4 start="(7, 9)" end="(7, 12)">
             <IdentNode4 start="(7, 9)" end="(7, 12)" leading="" trailing=" " raw_val="foo" val="foo"/>
             <NullNode4/>
           </CommandDeclidNode4>
           <CommandDeclsigNode4 start="(7, 13)" end="(7, 43)">
             <NullNode4 start="(7, 13)" end="(7, 22)">
               <TermExplicitbinderNode4 start="(7, 13)" end="(7, 22)">
                 <AtomNode4 start="(7, 13)" end="(7, 14)" leading="" trailing="" val="("/>
                 <NullNode4 start="(7, 14)" end="(7, 15)">
                   <IdentNode4 start="(7, 14)" end="(7, 15)" leading="" trailing=" " raw_val="a" val="a"/>
                 </NullNode4>
                 <NullNode4 start="(7, 16)" end="(7, 21)">
                   <AtomNode4 start="(7, 16)" end="(7, 17)" leading="" trailing=" " val=":"/>
                   <IdentNode4 start="(7, 18)" end="(7, 21)" leading="" trailing="" raw_val="Nat" val="Nat" full_name="Nat" mod_name="Init.Prelude" def_path=".lake/packages/lean4/src/lean/Init/Prelude.lean" def_start="(1044, 11)" def_end="(1044, 14)"/>
                 </NullNode4>
                 <NullNode4/>
                 <AtomNode4 start="(7, 21)" end="(7, 22)" leading="" trailing=" " val=")"/>
               </TermExplicitbinderNode4>
             </NullNode4>
             <TermTypespecNode4 start="(7, 23)" end="(7, 43)">
               <AtomNode4 start="(7, 23)" end="(7, 24)" leading="" trailing=" " val=":"/>
               <OtherNode4 start="(7, 25)" end="(7, 43)" kind="«term_=_»">
                 <OtherNode4 start="(7, 25)" end="(7, 30)" kind="«term_+_»">
                   <IdentNode4 start="(7, 25)" end="(7, 26)" leading="" trailing=" " raw_val="a" val="a"/>
                   <AtomNode4 start="(7, 27)" end="(7, 28)" leading="" trailing=" " val="+"/>
                   <OtherNode4 start="(7, 29)" end="(7, 30)" kind="num">
                     <AtomNode4 start="(7, 29)" end="(7, 30)" leading="" trailing=" " val="1"/>
                   </OtherNode4>
                 </OtherNode4>
                 <AtomNode4 start="(7, 31)" end="(7, 32)" leading="" trailing=" " val="="/>
                 <OtherNode4 start="(7, 33)" end="(7, 43)" kind="Lean.Parser.Term.app">
                   <IdentNode4 start="(7, 33)" end="(7, 41)" leading="" trailing=" " raw_val="Nat.succ" val="Nat.succ" full_name="Nat.succ" mod_name="Init.Prelude" def_path=".lake/packages/lean4/src/lean/Init/Prelude.lean" def_start="(1050, 5)" def_end="(1050, 9)"/>
                   <NullNode4 start="(7, 42)" end="(7, 43)">
                     <IdentNode4 start="(7, 42)" end="(7, 43)" leading="" trailing=" " raw_val="a" val="a"/>
                   </NullNode4>
                 </OtherNode4>
               </OtherNode4>
             </TermTypespecNode4>
           </CommandDeclsigNode4>
           <CommandDeclvalsimpleNode4 start="(7, 44)" end="(7, 53)">
             <AtomNode4 start="(7, 44)" end="(7, 46)" leading="" trailing=" " val=":="/>
             <TermBytacticNode4 start="(7, 47)" end="(7, 53)">
               <AtomNode4 start="(7, 47)" end="(7, 49)" leading="" trailing=" " val="by"/>
               <TacticTacticseqNode4 start="(7, 50)" end="(7, 53)">
                 <TacticTacticseq1IndentedNode4 start="(7, 50)" end="(7, 53)">
                   <NullNode4 start="(7, 50)" end="(7, 53)">
                     <OtherNode4 start="(7, 50)" end="(7, 53)" kind="Lean.Parser.Tactic.tacticRfl" state_before="a : Nat&#10;⊢ a + 1 = Nat.succ a" state_after="no goals" tactic="rfl">
                       <AtomNode4 start="(7, 50)" end="(7, 53)" leading="" trailing="&#10;" val="rfl"/>
                     </OtherNode4>
                   </NullNode4>
                 </TacticTacticseq1IndentedNode4>
               </TacticTacticseqNode4>
             </TermBytacticNode4>
             <NullNode4/>
           </CommandDeclvalsimpleNode4>
           <NullNode4/>
           <NullNode4/>
         </CommandTheoremNode4>
       </CommandDeclarationNode4>
     </FileNode4>
     <Comments/>
   </TracedFile>


Interacting with Lean 4
***********************

LeanDojo can also interact with Lean 4. Below we prove the :code:`hello_world` 
theorem in the previous example. Note that the `lean4-example <https://github.com/yangky11/lean4-example>`_ repo
has to be traced before interacting with any theorem in it. So the code below will first take some time 
to trace the repo if you haven't followed the steps in :ref:`extracting-data-from-lean4`.  The tracing has to be done 
only once, and the traced repo will be cached for future use. Some repos do not need to be traced locally and 
can be downloaded from `our AWS S3 <https://lean-dojo.s3.amazonaws.com>`_ (see :ref:`caching` for details).

.. code-block:: python

   from lean_dojo import *

   repo = LeanGitRepo("https://github.com/yangky11/lean4-example", "fd14c4c8b29cc74a082e5ae6f64c2fb25b28e15e")
   theorem = Theorem(repo, "Lean4Example.lean", "hello_world")

   with Dojo(theorem) as (dojo, init_state):
     print(init_state)
     result = dojo.run_tac(init_state, "rw [add_assoc, add_comm b, ←add_assoc]")
     assert isinstance(result, ProofFinished)
     print(result)

.. code-block::
   :caption: Expected output:

   TacticState(pp='a b c : Nat\n⊢ a + b + c = a + c + b', id=0, message=None)
   ProofFinished(tactic_state_id=1, message='')


Next Steps
**********

This example is just a glimpse of what LeanDojo can do. Please continue to the demos (`Lean 3 <https://github.com/lean-dojo/LeanDojo/blob/main/scripts/demo-lean3.ipynb>`_, `Lean 4 <https://github.com/lean-dojo/LeanDojo/blob/main/scripts/demo-lean4.ipynb>`_) and the :ref:`user-guide`.
